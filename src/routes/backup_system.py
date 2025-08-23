from flask import Blueprint, jsonify, send_file, render_template_string, request, redirect, url_for, session
import os
import json
import zipfile
import shutil
import subprocess
from datetime import datetime
from src.models import db, Image, Category, ImageCategory, SystemConfig
from src.config import PHOTOGRAPHY_ASSETS_DIR
import tempfile

backup_system_bp = Blueprint('backup_system', __name__)

@backup_system_bp.route('/admin/backup-system')
def backup_system_dashboard():
    """Backup system management dashboard"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    
    # Get system status
    image_count = Image.query.count()
    category_count = Category.query.count()
    
    # Check volume usage
    volume_files = []
    volume_size = 0
    if os.path.exists(PHOTOGRAPHY_ASSETS_DIR):
        for file in os.listdir(PHOTOGRAPHY_ASSETS_DIR):
            file_path = os.path.join(PHOTOGRAPHY_ASSETS_DIR, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                volume_size += size
                volume_files.append({
                    'name': file,
                    'size': size,
                    'size_mb': round(size / (1024 * 1024), 2)
                })
    
    # Format volume size
    volume_size_mb = round(volume_size / (1024 * 1024), 2)
    
    return render_template_string(backup_dashboard_html,
                                image_count=image_count,
                                category_count=category_count,
                                volume_files_count=len(volume_files),
                                volume_size_mb=volume_size_mb,
                                message=request.args.get('message'),
                                message_type=request.args.get('message_type', 'success'))

@backup_system_bp.route('/admin/backup/create-manual', methods=['POST'])
def create_manual_backup():
    """Create complete manual backup (images + data + database)"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"mindseye_backup_{timestamp}"
        
        # Create temporary directory for backup
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = os.path.join(temp_dir, backup_name)
            os.makedirs(backup_dir)
            
            # 1. Backup database
            db_backup_path = os.path.join(backup_dir, 'database')
            os.makedirs(db_backup_path)
            
            # Export all data to JSON
            backup_data = {
                'timestamp': timestamp,
                'version': '1.0',
                'images': [],
                'categories': [],
                'system_config': []
            }
            
            # Export images
            for image in Image.query.all():
                image_data = {
                    'id': image.id,
                    'filename': image.filename,
                    'title': image.title,
                    'description': image.description,
                    'file_size': image.file_size,
                    'width': image.width,
                    'height': image.height,
                    'upload_date': image.upload_date.isoformat() if image.upload_date else None,
                    'categories': [cat.category.name for cat in image.categories]
                }
                backup_data['images'].append(image_data)
            
            # Export categories
            for category in Category.query.all():
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'display_order': category.display_order
                }
                backup_data['categories'].append(category_data)
            
            # Export system config
            for config in SystemConfig.query.all():
                config_data = {
                    'key': config.key,
                    'value': config.value,
                    'data_type': config.data_type,
                    'description': config.description
                }
                backup_data['system_config'].append(config_data)
            
            # Save backup data
            with open(os.path.join(db_backup_path, 'backup_data.json'), 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            # Copy database file
            db_file = os.path.join(PHOTOGRAPHY_ASSETS_DIR, 'mindseye.db')
            if os.path.exists(db_file):
                shutil.copy2(db_file, os.path.join(db_backup_path, 'mindseye.db'))
            
            # 2. Backup images
            images_backup_path = os.path.join(backup_dir, 'images')
            os.makedirs(images_backup_path)
            
            if os.path.exists(PHOTOGRAPHY_ASSETS_DIR):
                for file in os.listdir(PHOTOGRAPHY_ASSETS_DIR):
                    file_path = os.path.join(PHOTOGRAPHY_ASSETS_DIR, file)
                    if os.path.isfile(file_path) and not file.endswith('.db'):
                        shutil.copy2(file_path, images_backup_path)
            
            # 3. Backup source code
            code_backup_path = os.path.join(backup_dir, 'source_code')
            os.makedirs(code_backup_path)
            
            # Copy main source files
            src_dir = os.path.dirname(os.path.dirname(__file__))
            for item in ['src', 'requirements.txt', 'README.md']:
                src_path = os.path.join(src_dir, item)
                if os.path.exists(src_path):
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, os.path.join(code_backup_path, item))
                    else:
                        shutil.copy2(src_path, code_backup_path)
            
            # 4. Create restore instructions
            restore_instructions = create_restore_instructions()
            with open(os.path.join(backup_dir, 'RESTORE_INSTRUCTIONS.md'), 'w') as f:
                f.write(restore_instructions)
            
            # 5. Create backup info
            backup_info = {
                'backup_name': backup_name,
                'timestamp': timestamp,
                'image_count': len(backup_data['images']),
                'category_count': len(backup_data['categories']),
                'total_files': len(os.listdir(images_backup_path)) if os.path.exists(images_backup_path) else 0,
                'backup_size_mb': get_directory_size(backup_dir) / (1024 * 1024)
            }
            
            with open(os.path.join(backup_dir, 'backup_info.json'), 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            # 6. Create ZIP file
            zip_path = os.path.join(temp_dir, f"{backup_name}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
            
            # Return the ZIP file for download
            return send_file(zip_path, 
                           as_attachment=True, 
                           download_name=f"{backup_name}.zip",
                           mimetype='application/zip')
    
    except Exception as e:
        return redirect(url_for('backup_system.backup_system_dashboard', 
                              message=f"Backup failed: {str(e)}", 
                              message_type='error'))

@backup_system_bp.route('/admin/backup/github-push', methods=['POST'])
def github_backup_push():
    """Push current state to GitHub with backup tag"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        tag_name = f"backup-{timestamp}"
        
        # Get current directory (should be project root)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Git commands
        commands = [
            ['git', 'add', '.'],
            ['git', 'commit', '-m', f'🛡️ BACKUP: Automated backup {timestamp}', '--allow-empty'],
            ['git', 'tag', tag_name],
            ['git', 'push', 'origin', 'main', '--tags']
        ]
        
        for cmd in commands:
            result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Git command failed: {' '.join(cmd)}\n{result.stderr}")
        
        return redirect(url_for('backup_system.backup_system_dashboard',
                              message=f"GitHub backup created successfully! Tag: {tag_name}",
                              message_type='success'))
    
    except Exception as e:
        return redirect(url_for('backup_system.backup_system_dashboard',
                              message=f"GitHub backup failed: {str(e)}",
                              message_type='error'))

@backup_system_bp.route('/admin/backup/restore-guide')
def restore_guide():
    """Display restore instructions"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    
    instructions = create_restore_instructions()
    return render_template_string(restore_guide_html, instructions=instructions)

def get_directory_size(directory):
    """Calculate total size of directory"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def create_restore_instructions():
    """Create comprehensive restore instructions"""
    return """# Mind's Eye Photography - Disaster Recovery Guide

## 🚨 EMERGENCY RESTORE PROCEDURES

### SCENARIO 1: Complete System Restore from Backup ZIP

1. **Download your backup ZIP file** (from manual backup)
2. **Extract the ZIP file** to a temporary location
3. **Stop the current application** (if running)

#### Restore Database:
```bash
# Copy database file
cp backup_folder/database/mindseye.db /data/mindseye.db

# Or restore from JSON data
# Use the backup_data.json file to recreate database
```

#### Restore Images:
```bash
# Copy all images to volume
cp backup_folder/images/* /data/
```

#### Restore Source Code:
```bash
# Replace current source with backup
rm -rf src/
cp -r backup_folder/source_code/src ./
```

### SCENARIO 2: Restore from GitHub Backup

1. **Find your backup tag** in GitHub repository
2. **Clone or checkout the backup tag**:
```bash
git clone https://github.com/your-repo/Minds-eye-master.git
cd Minds-eye-master
git checkout backup-YYYYMMDD_HHMMSS
```

3. **Deploy to Railway** using the backup version

### SCENARIO 3: Database-Only Recovery

If only database is corrupted but images are safe:

1. **Use backup_data.json** from your backup
2. **Run database restore script**:
```python
# Import backup data and recreate database
python restore_database.py backup_data.json
```

### SCENARIO 4: Images-Only Recovery

If database is fine but images are lost:

1. **Copy images from backup**:
```bash
cp backup_folder/images/* /data/
```

2. **Run image migration**:
```bash
# Access admin panel and use force migration
/debug/force-migration
```

## 🛡️ PREVENTION TIPS

- **Regular backups**: Use manual backup weekly
- **GitHub backups**: Push backup tags monthly  
- **Test restores**: Verify backup integrity quarterly
- **Monitor volume**: Check `/data` directory regularly

## 📞 EMERGENCY CONTACTS

- **Railway Support**: For volume/deployment issues
- **GitHub Support**: For repository problems
- **Backup Location**: Store backups in multiple locations

## ⚡ QUICK RECOVERY CHECKLIST

- [ ] Identify what was lost (database, images, code)
- [ ] Locate most recent backup
- [ ] Stop current application
- [ ] Restore from backup
- [ ] Test functionality
- [ ] Create new backup after recovery

**Remember: Your backups are only as good as your last test restore!**
"""

# HTML Templates
backup_dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Backup System - Mind's Eye Photography</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .backup-section { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .status-card { background: #3d3d3d; padding: 15px; border-radius: 8px; text-align: center; }
        .status-number { font-size: 2em; font-weight: bold; color: #4CAF50; }
        .backup-btn { background: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; margin: 10px; font-size: 16px; }
        .backup-btn:hover { background: #45a049; }
        .github-btn { background: #333; }
        .github-btn:hover { background: #555; }
        .restore-btn { background: #ff9800; }
        .restore-btn:hover { background: #e68900; }
        .danger-btn { background: #f44336; }
        .danger-btn:hover { background: #da190b; }
        .message { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .success { background: #4CAF50; }
        .error { background: #f44336; }
        .nav-link { color: #4CAF50; text-decoration: none; margin-right: 20px; }
        .nav-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Backup System - Mind's Eye Photography</h1>
            <nav>
                <a href="/admin/dashboard" class="nav-link">← Back to Admin Dashboard</a>
                <a href="/admin/backup/restore-guide" class="nav-link">📋 Restore Guide</a>
            </nav>
        </div>

        {% if message %}
        <div class="message {{ message_type }}">
            {{ message }}
        </div>
        {% endif %}

        <div class="backup-section">
            <h2>📊 System Status</h2>
            <div class="status-grid">
                <div class="status-card">
                    <div class="status-number">{{ image_count }}</div>
                    <div>Images in Database</div>
                </div>
                <div class="status-card">
                    <div class="status-number">{{ category_count }}</div>
                    <div>Categories</div>
                </div>
                <div class="status-card">
                    <div class="status-number">{{ volume_files_count }}</div>
                    <div>Files in Volume</div>
                </div>
                <div class="status-card">
                    <div class="status-number">{{ volume_size_mb }}</div>
                    <div>Volume Size (MB)</div>
                </div>
            </div>
        </div>

        <div class="backup-section">
            <h2>💾 Manual Backup</h2>
            <p>Create a complete backup including images, database, and source code.</p>
            <form method="POST" action="/admin/backup/create-manual">
                <button type="submit" class="backup-btn">📥 Create Complete Backup</button>
            </form>
            <small>Downloads a ZIP file with everything needed for disaster recovery.</small>
        </div>

        <div class="backup-section">
            <h2>🔄 GitHub Backup</h2>
            <p>Push current state to GitHub repository with backup tag.</p>
            <form method="POST" action="/admin/backup/github-push">
                <button type="submit" class="backup-btn github-btn">📤 Push to GitHub</button>
            </form>
            <small>Creates a tagged backup in your GitHub repository.</small>
        </div>

        <div class="backup-section">
            <h2>🚨 Disaster Recovery</h2>
            <p>Emergency restore procedures and instructions.</p>
            <a href="/admin/backup/restore-guide" class="backup-btn restore-btn">📋 View Restore Guide</a>
            <small>Step-by-step instructions for emergency recovery.</small>
        </div>

        <div class="backup-section">
            <h2>⚙️ Advanced Options</h2>
            <p>Debug and maintenance tools.</p>
            <a href="/debug/volume-info" class="backup-btn">🔍 Volume Info</a>
            <a href="/debug/database-info" class="backup-btn">📊 Database Info</a>
            <a href="/debug/force-migration" class="backup-btn">🔄 Force Migration</a>
        </div>
    </div>
</body>
</html>
'''

restore_guide_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Restore Guide - Mind's Eye Photography</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .content { background: #2d2d2d; padding: 20px; border-radius: 8px; }
        pre { background: #1a1a1a; padding: 15px; border-radius: 5px; overflow-x: auto; }
        code { background: #3d3d3d; padding: 2px 5px; border-radius: 3px; }
        h1, h2, h3 { color: #4CAF50; }
        .nav-link { color: #4CAF50; text-decoration: none; margin-right: 20px; }
        .nav-link:hover { text-decoration: underline; }
        .warning { background: #ff9800; color: #000; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .danger { background: #f44336; padding: 10px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Disaster Recovery Guide</h1>
            <nav>
                <a href="/admin/backup-system" class="nav-link">← Back to Backup System</a>
                <a href="/admin/dashboard" class="nav-link">🏠 Admin Dashboard</a>
            </nav>
        </div>

        <div class="content">
            <div class="danger">
                <strong>⚠️ EMERGENCY USE ONLY:</strong> These procedures should only be used in case of data loss or system failure.
            </div>
            
            <pre>{{ instructions }}</pre>
        </div>
    </div>
</body>
</html>
'''


#!/usr/bin/env python3
"""
Direct database cleanup script - removes hex codes and "Migrated from volume" text
"""

import sys
import os
import re
import sqlite3

# Database path
DATABASE_PATH = '/data/mindseye.db'

def cleanup_database():
    """Clean up database titles and descriptions directly"""
    try:
        print('🔄 Starting direct database cleanup...')
        
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get all images
        cursor.execute('SELECT id, title, description FROM image')
        images = cursor.fetchall()
        
        updated_count = 0
        
        print(f'📊 Found {len(images)} images in database')
        
        for image_id, title, description in images:
            original_title = title
            original_description = description
            
            # Remove hex codes from title (pattern: space + 6-8 hex characters at end)
            if title:
                clean_title = re.sub(r'\s+[A-F0-9]{6,8}$', '', title, flags=re.IGNORECASE)
                title = clean_title.strip()
            
            # Remove 'Migrated from volume - ' prefix from description
            if description and description.startswith('Migrated from volume - '):
                description = description.replace('Migrated from volume - ', '').strip()
            
            # Update if anything changed
            if original_title != title or original_description != description:
                cursor.execute(
                    'UPDATE image SET title = ?, description = ? WHERE id = ?',
                    (title, description, image_id)
                )
                updated_count += 1
                print(f'✅ Updated: "{original_title}" -> "{title}"')
        
        # Commit changes
        conn.commit()
        
        # Add indexes for better performance
        try:
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_image_title ON image(title)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_image_upload_date ON image(upload_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_image_category_image_id ON image_category(image_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_image_category_category_id ON image_category(category_id)')
            conn.commit()
            print('🚀 Database indexes optimized')
        except Exception as e:
            print(f'ℹ️  Index optimization note: {e}')
        
        conn.close()
        
        print(f'🎉 Database cleanup complete! Updated {updated_count} images')
        return True
        
    except Exception as e:
        print(f'❌ Cleanup error: {e}')
        return False

if __name__ == '__main__':
    success = cleanup_database()
    if success:
        print('✅ Database cleanup successful!')
    else:
        print('❌ Database cleanup failed!')


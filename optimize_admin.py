#!/usr/bin/env python3
"""
Script to optimize admin performance and clean up database
"""

import sys
import os
import re

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app
from models import db, Image

def optimize_and_cleanup():
    with app.app_context():
        print('🔄 Optimizing admin performance and cleaning up database...')
        
        # Get all images
        images = Image.query.all()
        updated_count = 0
        
        for image in images:
            original_title = image.title
            original_description = image.description
            
            # Remove hex codes from title (pattern: space + 6-8 hex characters at end)
            if image.title:
                clean_title = re.sub(r'\s+[A-F0-9]{6,8}$', '', image.title, flags=re.IGNORECASE)
                image.title = clean_title.strip()
            
            # Remove 'Migrated from volume - ' prefix from description
            if image.description and image.description.startswith('Migrated from volume - '):
                image.description = image.description.replace('Migrated from volume - ', '').strip()
            
            # Check if anything changed
            if original_title != image.title or original_description != image.description:
                updated_count += 1
                print(f'✅ Updated: "{original_title}" -> "{image.title}"')
        
        # Commit changes
        db.session.commit()
        print(f'🎉 Successfully cleaned up {updated_count} images!')
        print(f'📊 Total images in database: {len(images)}')
        
        # Add database indexes for better performance
        try:
            # These will be created if they don't exist
            db.engine.execute('CREATE INDEX IF NOT EXISTS idx_image_title ON image(title)')
            db.engine.execute('CREATE INDEX IF NOT EXISTS idx_image_upload_date ON image(upload_date)')
            db.engine.execute('CREATE INDEX IF NOT EXISTS idx_image_categories ON image_category(image_id)')
            print('✅ Database indexes optimized for better performance')
        except Exception as e:
            print(f'ℹ️  Index optimization: {e}')

if __name__ == '__main__':
    optimize_and_cleanup()


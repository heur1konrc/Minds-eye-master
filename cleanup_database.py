#!/usr/bin/env python3
"""
Script to clean up image titles and descriptions in the database
- Remove hex codes from titles
- Remove "Migrated from volume - " prefix from descriptions
"""

import sys
import os
import re

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app
from models import db, Image

def cleanup_database():
    with app.app_context():
        print('🔄 Cleaning up image titles and descriptions...')
        
        # Get all images
        images = Image.query.all()
        updated_count = 0
        
        for image in images:
            original_title = image.title
            original_description = image.description
            
            # Remove hex codes from title (pattern: space + 6-8 hex characters at end)
            if image.title:
                # Remove patterns like ' 51B3A3A0', ' F649D6D6', etc.
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

if __name__ == '__main__':
    cleanup_database()


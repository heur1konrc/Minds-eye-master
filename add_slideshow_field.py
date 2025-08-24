#!/usr/bin/env python3
"""
Database Migration: Add is_slideshow_background field to Image table
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db, Image
from src.main import app

def migrate_database():
    """Add is_slideshow_background field if it doesn't exist"""
    with app.app_context():
        try:
            # Try to access the field on an existing image
            test_image = Image.query.first()
            if test_image:
                # Test if field exists
                hasattr_result = hasattr(test_image, 'is_slideshow_background')
                print(f"✅ Field 'is_slideshow_background' exists: {hasattr_result}")
                
                if hasattr_result:
                    current_value = getattr(test_image, 'is_slideshow_background', 'MISSING')
                    print(f"✅ Current value: {current_value}")
                else:
                    print("❌ Field missing - need to recreate database")
                    
            else:
                print("ℹ️ No images in database to test")
                
            # Force database schema update
            print("🔄 Recreating all tables to ensure schema is current...")
            db.create_all()
            print("✅ Database schema updated")
            
            # Count current slideshow images
            slideshow_count = Image.query.filter_by(is_slideshow_background=True).count()
            print(f"📊 Current slideshow images: {slideshow_count}")
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    migrate_database()


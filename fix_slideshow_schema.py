#!/usr/bin/env python3
"""
Database Schema Fix: Ensure is_slideshow_background field exists
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db, Image
from src.main import app
from sqlalchemy import text

def fix_slideshow_schema():
    """Add is_slideshow_background field if it doesn't exist"""
    with app.app_context():
        try:
            print("🔍 Checking slideshow field schema...")
            
            # Test if field exists by trying to query it
            try:
                test_query = db.session.execute(
                    text("SELECT is_slideshow_background FROM image LIMIT 1")
                )
                print("✅ Field 'is_slideshow_background' exists in database")
                
                # Count current slideshow images
                slideshow_count = Image.query.filter_by(is_slideshow_background=True).count()
                print(f"📊 Current slideshow images: {slideshow_count}")
                
                # List slideshow images
                slideshow_images = Image.query.filter_by(is_slideshow_background=True).all()
                for img in slideshow_images:
                    print(f"  - {img.title} (ID: {img.id})")
                    
            except Exception as field_error:
                print(f"❌ Field missing or inaccessible: {field_error}")
                print("🔧 Adding is_slideshow_background field...")
                
                # Add the field using raw SQL
                try:
                    db.session.execute(
                        text("ALTER TABLE image ADD COLUMN is_slideshow_background BOOLEAN DEFAULT FALSE")
                    )
                    db.session.commit()
                    print("✅ Field added successfully")
                    
                    # Verify the field was added
                    test_query = db.session.execute(
                        text("SELECT is_slideshow_background FROM image LIMIT 1")
                    )
                    print("✅ Field verification successful")
                    
                except Exception as add_error:
                    print(f"❌ Failed to add field: {add_error}")
                    db.session.rollback()
                    
                    # Try alternative approach - recreate tables
                    print("🔧 Trying alternative approach - recreate tables...")
                    try:
                        db.create_all()
                        print("✅ Tables recreated successfully")
                    except Exception as create_error:
                        print(f"❌ Table recreation failed: {create_error}")
            
            # Test a simple update operation
            try:
                print("🧪 Testing slideshow field update...")
                first_image = Image.query.first()
                if first_image:
                    original_value = getattr(first_image, 'is_slideshow_background', False)
                    print(f"🔍 Original value: {original_value}")
                    
                    # Test update
                    first_image.is_slideshow_background = True
                    db.session.commit()
                    print("✅ Update test successful")
                    
                    # Revert
                    first_image.is_slideshow_background = original_value
                    db.session.commit()
                    print("✅ Revert test successful")
                else:
                    print("ℹ️ No images to test with")
                    
            except Exception as update_error:
                print(f"❌ Update test failed: {update_error}")
                db.session.rollback()
                
        except Exception as e:
            print(f"❌ Schema fix error: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    fix_slideshow_schema()


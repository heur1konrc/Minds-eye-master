#!/usr/bin/env python3
"""
Debug script to test slideshow field in production database
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db, Image
from src.main import app

def debug_slideshow_field():
    """Test if is_slideshow_background field exists and works"""
    with app.app_context():
        try:
            print("🔍 Testing slideshow field...")
            
            # Get first image
            first_image = Image.query.first()
            if not first_image:
                print("❌ No images in database")
                return
                
            print(f"✅ Found image: {first_image.title}")
            print(f"✅ Image ID: {first_image.id}")
            
            # Test if field exists
            try:
                current_value = first_image.is_slideshow_background
                print(f"✅ Field exists! Current value: {current_value}")
            except AttributeError as e:
                print(f"❌ Field missing: {e}")
                return
            except Exception as e:
                print(f"❌ Field access error: {e}")
                return
                
            # Test updating the field
            try:
                print("🔄 Testing field update...")
                original_value = first_image.is_slideshow_background
                first_image.is_slideshow_background = not original_value
                db.session.commit()
                print(f"✅ Update successful: {original_value} -> {first_image.is_slideshow_background}")
                
                # Revert the change
                first_image.is_slideshow_background = original_value
                db.session.commit()
                print(f"✅ Reverted to original: {first_image.is_slideshow_background}")
                
            except Exception as e:
                print(f"❌ Update failed: {e}")
                db.session.rollback()
                
            # Count slideshow images
            try:
                slideshow_count = Image.query.filter_by(is_slideshow_background=True).count()
                print(f"📊 Current slideshow images: {slideshow_count}")
                
                # List slideshow images
                slideshow_images = Image.query.filter_by(is_slideshow_background=True).all()
                for img in slideshow_images:
                    print(f"  - {img.title} (ID: {img.id})")
                    
            except Exception as e:
                print(f"❌ Query failed: {e}")
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    debug_slideshow_field()


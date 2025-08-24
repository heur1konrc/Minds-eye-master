#!/usr/bin/env python3
"""
Simple test to replicate the slideshow toggle API functionality
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db, Image
from src.main import app
import json

def test_slideshow_toggle():
    """Test the slideshow toggle functionality directly"""
    with app.app_context():
        try:
            print("🔍 Testing slideshow toggle functionality...")
            
            # Get first image to test with
            test_image = Image.query.first()
            if not test_image:
                print("❌ No images in database to test")
                return
                
            print(f"✅ Testing with image: {test_image.title} (ID: {test_image.id})")
            
            # Test the exact logic from the API endpoint
            try:
                # Get current status
                current_status = getattr(test_image, 'is_slideshow_background', None)
                print(f"✅ Current slideshow status: {current_status}")
                
                # Test boolean conversion (this might be the issue)
                new_status = True  # Simulate adding to slideshow
                print(f"🔄 Setting new status to: {new_status}")
                
                # Update the field
                test_image.is_slideshow_background = new_status
                
                # Commit to database
                db.session.commit()
                print(f"✅ Database update successful!")
                
                # Verify the change
                updated_image = Image.query.get(test_image.id)
                final_status = updated_image.is_slideshow_background
                print(f"✅ Verified new status: {final_status}")
                
                # Count slideshow images
                slideshow_count = Image.query.filter_by(is_slideshow_background=True).count()
                print(f"📊 Total slideshow images: {slideshow_count}")
                
                # Test JSON response format
                response_data = {
                    'success': True,
                    'message': f'Image {"added to" if new_status else "removed from"} slideshow',
                    'image_id': test_image.id,
                    'new_status': final_status,
                    'slideshow_count': slideshow_count
                }
                print(f"✅ JSON response: {json.dumps(response_data, indent=2)}")
                
            except Exception as e:
                print(f"❌ Slideshow toggle failed: {e}")
                print(f"❌ Error type: {type(e).__name__}")
                import traceback
                print(f"❌ Full traceback: {traceback.format_exc()}")
                db.session.rollback()
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    test_slideshow_toggle()


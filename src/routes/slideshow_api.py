"""
Simple Slideshow API Routes (Option 1)
Uses existing Image table with is_slideshow_background field
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for
from ..models import db, Image

slideshow_api_bp = Blueprint('slideshow_api', __name__)

@slideshow_api_bp.route('/api/slideshow-images')
def get_slideshow_images():
    """Get images marked for slideshow background"""
    try:
        # Get images marked for slideshow (limit to 5 for performance)
        slideshow_images = Image.query.filter_by(is_slideshow_background=True).limit(5).all()
        
        images_data = []
        for image in slideshow_images:
            images_data.append({
                'id': image.id,
                'filename': image.filename,
                'title': image.title,
                'url': f'https://minds-eye-master-production.up.railway.app/static/assets/{image.filename}'
            })
        
        return jsonify({
            'success': True,
            'images': images_data,
            'count': len(images_data)
        })
        
    except Exception as e:
        print(f"Slideshow API error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to load slideshow images',
            'images': []
        }), 500

@slideshow_api_bp.route('/admin/slideshow-toggle', methods=['POST'])
def toggle_slideshow_image():
    """Toggle slideshow status for an image"""
    print(f"🔍 Slideshow toggle called - Session: {session.get('admin_logged_in')}")
    
    if not session.get('admin_logged_in'):
        print("❌ Not authenticated")
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        print(f"🔍 Request data: {data}")
        
        image_id = data.get('image_id')
        is_slideshow = data.get('is_slideshow', False)
        
        print(f"🔍 Parsed - image_id: {image_id}, is_slideshow: {is_slideshow}")
        
        if not image_id:
            print("❌ No image ID provided")
            return jsonify({'success': False, 'message': 'Image ID required'}), 400
        
        # Check current slideshow count if trying to add
        if is_slideshow:
            current_count = Image.query.filter_by(is_slideshow_background=True).count()
            print(f"🔍 Current slideshow count: {current_count}")
            if current_count >= 5:
                return jsonify({
                    'success': False, 
                    'message': 'Maximum 5 images allowed in slideshow. Remove one first.'
                }), 400
        
        # Find and update the image
        image = Image.query.get(image_id)
        print(f"🔍 Found image: {image}")
        
        if not image:
            print("❌ Image not found")
            return jsonify({'success': False, 'message': 'Image not found'}), 404
        
        image.is_slideshow_background = is_slideshow
        db.session.commit()
        print(f"✅ Updated image slideshow status to: {is_slideshow}")
        
        action = 'added to' if is_slideshow else 'removed from'
        return jsonify({
            'success': True,
            'message': f'Image {action} slideshow successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Slideshow toggle error: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


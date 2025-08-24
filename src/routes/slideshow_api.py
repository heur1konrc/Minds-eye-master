"""
Slideshow Background API Routes
Handles slideshow background image management and settings
"""

from flask import Blueprint, request, jsonify
from ..models import db, Image, SlideshowBackground, SlideshowSettings
from sqlalchemy import func

slideshow_bp = Blueprint('slideshow', __name__)

@slideshow_bp.route('/api/slideshow/backgrounds', methods=['GET'])
def get_slideshow_backgrounds():
    """Get all slideshow background images in order"""
    try:
        backgrounds = db.session.query(SlideshowBackground)\
            .join(Image)\
            .filter(SlideshowBackground.is_active == True)\
            .order_by(SlideshowBackground.display_order)\
            .all()
        
        background_list = []
        for bg in backgrounds:
            if bg.image:
                background_list.append({
                    'id': bg.id,
                    'image_id': bg.image_id,
                    'filename': bg.image.filename,
                    'title': bg.image.title,
                    'display_order': bg.display_order,
                    'url': f'/assets/{bg.image.filename}'
                })
        
        return jsonify({
            'success': True,
            'backgrounds': background_list,
            'count': len(background_list)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@slideshow_bp.route('/api/slideshow/settings', methods=['GET'])
def get_slideshow_settings():
    """Get slideshow configuration settings"""
    try:
        settings = SlideshowSettings.query.first()
        if not settings:
            # Create default settings
            settings = SlideshowSettings(
                transition_duration=5000,
                fade_duration=1000,
                auto_play=True,
                pause_on_hover=True
            )
            db.session.add(settings)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'settings': settings.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@slideshow_bp.route('/api/slideshow/settings', methods=['POST'])
def update_slideshow_settings():
    """Update slideshow configuration settings"""
    try:
        data = request.get_json()
        
        settings = SlideshowSettings.query.first()
        if not settings:
            settings = SlideshowSettings()
            db.session.add(settings)
        
        # Update settings
        if 'transition_duration' in data:
            settings.transition_duration = int(data['transition_duration'])
        if 'fade_duration' in data:
            settings.fade_duration = int(data['fade_duration'])
        if 'auto_play' in data:
            settings.auto_play = bool(data['auto_play'])
        if 'pause_on_hover' in data:
            settings.pause_on_hover = bool(data['pause_on_hover'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Slideshow settings updated successfully',
            'settings': settings.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@slideshow_bp.route('/api/slideshow/backgrounds', methods=['POST'])
def add_slideshow_background():
    """Add image to slideshow backgrounds"""
    try:
        data = request.get_json()
        image_id = data.get('image_id')
        
        if not image_id:
            return jsonify({
                'success': False,
                'error': 'Image ID is required'
            }), 400
        
        # Check if image exists
        image = Image.query.get(image_id)
        if not image:
            return jsonify({
                'success': False,
                'error': 'Image not found'
            }), 404
        
        # Check if already in slideshow
        existing = SlideshowBackground.query.filter_by(
            image_id=image_id, 
            is_active=True
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Image already in slideshow'
            }), 400
        
        # Get next display order
        max_order = db.session.query(func.max(SlideshowBackground.display_order)).scalar() or 0
        
        # Add to slideshow
        slideshow_bg = SlideshowBackground(
            image_id=image_id,
            display_order=max_order + 1,
            is_active=True
        )
        
        db.session.add(slideshow_bg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image added to slideshow',
            'background': slideshow_bg.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@slideshow_bp.route('/api/slideshow/backgrounds/<int:bg_id>', methods=['DELETE'])
def remove_slideshow_background(bg_id):
    """Remove image from slideshow backgrounds"""
    try:
        background = SlideshowBackground.query.get(bg_id)
        if not background:
            return jsonify({
                'success': False,
                'error': 'Background not found'
            }), 404
        
        background.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image removed from slideshow'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@slideshow_bp.route('/api/slideshow/backgrounds/reorder', methods=['POST'])
def reorder_slideshow_backgrounds():
    """Reorder slideshow background images"""
    try:
        data = request.get_json()
        background_ids = data.get('background_ids', [])
        
        if not background_ids:
            return jsonify({
                'success': False,
                'error': 'Background IDs are required'
            }), 400
        
        # Update display order for each background
        for index, bg_id in enumerate(background_ids):
            background = SlideshowBackground.query.get(bg_id)
            if background:
                background.display_order = index + 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Slideshow order updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


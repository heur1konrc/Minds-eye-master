#!/usr/bin/env python3
"""
Trigger database cleanup on production via API endpoint
"""

import requests
import json

def trigger_cleanup():
    """Trigger database cleanup on production Railway instance"""
    
    # Create cleanup endpoint URL
    base_url = "https://minds-eye-master-production.up.railway.app"
    
    print('🔄 Triggering database cleanup on production...')
    
    try:
        # Make request to trigger cleanup
        response = requests.get(f"{base_url}/api/cleanup-database", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f'✅ Cleanup successful!')
            print(f'   • Updated {result.get("updated_count", 0)} images')
            print(f'   • Total images: {result.get("total_images", 0)}')
            print(f'   • Database optimized: {result.get("optimized", False)}')
        else:
            print(f'❌ Cleanup failed: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'❌ Error triggering cleanup: {e}')

if __name__ == '__main__':
    trigger_cleanup()


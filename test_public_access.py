#!/usr/bin/env python3
"""
Quick test to verify public access routes work correctly
"""
from app import create_app
from models import db

def test_routes():
    """Test that routes are configured correctly"""
    app = create_app()
    
    with app.app_context():
        # Get all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
                'path': str(rule)
            })
        
        # Sort by path
        routes.sort(key=lambda x: x['path'])
        
        print("\n" + "="*70)
        print("REGISTERED ROUTES")
        print("="*70)
        print(f"{'Path':<40} {'Methods':<15} {'Endpoint':<30}")
        print("-"*70)
        
        for route in routes:
            print(f"{route['path']:<40} {route['methods']:<15} {route['endpoint']:<30}")
        
        print("="*70)
        print(f"\nTotal routes: {len(routes)}")
        
        # Check key routes
        print("\n" + "="*70)
        print("KEY ROUTES VERIFICATION")
        print("="*70)
        
        key_routes = {
            '/': 'Public homepage (should redirect to /overview)',
            '/overview': 'Public leaderboard (no auth required)',
            '/manage': 'Management dashboard (auth required)',
            '/login': 'Login page',
            '/manage/events': 'Events list (auth required)',
            '/manage/admin/managers': 'Manager management (admin only)',
            '/manage/admin/logs': 'Activity logs (admin only)',
        }
        
        for path, description in key_routes.items():
            found = any(r['path'] == path for r in routes)
            status = "✅" if found else "❌"
            print(f"{status} {path:<30} - {description}")
        
        print("="*70)

if __name__ == '__main__':
    test_routes()

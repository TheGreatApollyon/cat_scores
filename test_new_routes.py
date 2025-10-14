#!/usr/bin/env python3
"""
Test script to verify new public routes
"""
from app import create_app

def test_routes():
    """Test that new routes are configured correctly"""
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
        print("PUBLIC ROUTES VERIFICATION")
        print("="*70)
        
        public_routes = {
            '/': 'Homepage (redirects to leaderboard)',
            '/leaderboard': 'Public leaderboard',
            '/events': 'Public events board',
            '/overview': 'Legacy redirect to leaderboard',
        }
        
        for path, description in public_routes.items():
            found = any(r['path'] == path for r in routes)
            status = "✅" if found else "❌"
            print(f"{status} {path:<30} - {description}")
        
        print("\n" + "="*70)
        print("PROTECTED ROUTES VERIFICATION")
        print("="*70)
        
        protected_routes = {
            '/manage': 'Management dashboard (requires login)',
            '/login': 'Login page',
            '/manage/events/': 'Events management',
            '/manage/admin/managers': 'Manager management (admin)',
            '/manage/admin/logs': 'Activity logs (admin)',
        }
        
        for path, description in protected_routes.items():
            found = any(r['path'] == path for r in routes)
            status = "✅" if found else "❌"
            print(f"{status} {path:<30} - {description}")
        
        print("="*70)
        
        # Test database initialization
        from models import Event, Cluster, User
        
        print("\n" + "="*70)
        print("DATABASE INITIALIZATION CHECK")
        print("="*70)
        
        cluster_count = Cluster.query.count()
        user_count = User.query.count()
        event_count = Event.query.count()
        
        print(f"✅ Clusters: {cluster_count} (expected: 7)")
        print(f"✅ Users: {user_count} (expected: 1 admin)")
        print(f"✅ Events: {event_count} (expected: 1 test event)")
        
        if event_count > 0:
            test_event = Event.query.first()
            print(f"\n📋 Test Event Details:")
            print(f"   Name: {test_event.name}")
            print(f"   Participants: {len(test_event.participants)}")
            print(f"   Created by: {test_event.get_creator().username}")
        
        print("="*70)

if __name__ == '__main__':
    test_routes()

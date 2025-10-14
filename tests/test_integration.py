import pytest
from models import User, Cluster, Event, Participant, ActivityLog, db
from app import create_app

@pytest.fixture
def app():
    """Create test application"""
    # Create app with test config BEFORE calling create_app
    from flask import Flask
    from flask_wtf.csrf import CSRFProtect
    from config import Config
    import os
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    app.config.from_object(Config)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize extensions
    csrf = CSRFProtect(app)
    db.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.events import events_bp
    from routes.overview import overview_bp
    from routes.logs import logs_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(overview_bp)
    app.register_blueprint(logs_bp)
    
    with app.app_context():
        db.create_all()
        
        # Create test clusters (7 predefined)
        clusters = [
            Cluster(name='Suryantra'),
            Cluster(name='Chandraloka'),
            Cluster(name='Swarnika'),
            Cluster(name='Ushnavi'),
            Cluster(name='Taraksha'),
            Cluster(name='Maya'),
            Cluster(name='Meghora')
        ]
        for cluster in clusters:
            db.session.add(cluster)
        
        # Create test users
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        manager = User(username='manager', role='event_manager')
        manager.set_password('manager123')
        db.session.add(manager)
        
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

# Authentication Flow Tests
def test_successful_login(client):
    """Test successful login with valid credentials"""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome' in response.data or b'Overview' in response.data

def test_failed_login_invalid_credentials(client):
    """Test failed login with invalid credentials"""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrongpassword'
    })
    
    assert b'Invalid username or password' in response.data

def test_session_persistence(client):
    """Test session persistence across requests"""
    # Login
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Access protected route
    response = client.get('/overview')
    assert response.status_code == 200

def test_logout_functionality(client):
    """Test logout functionality"""
    # Login first
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out' in response.data or b'Login' in response.data
    
    # Try to access protected route
    response = client.get('/overview', follow_redirects=True)
    assert b'log in' in response.data or b'Login' in response.data

def test_unauthorized_access_redirect(client):
    """Test unauthorized access redirects"""
    response = client.get('/events', follow_redirects=True)
    assert b'log in' in response.data or b'Login' in response.data

# Event Manager CRUD Tests
def test_admin_create_event_manager(client, app):
    """Test admin creating Event Manager account"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Create Event Manager
    response = client.post('/admin/managers/create', data={
        'username': 'newmanager',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify user was created
    with app.app_context():
        user = User.query.filter_by(username='newmanager').first()
        assert user is not None
        assert user.role == 'event_manager'

def test_admin_update_event_manager(client, app):
    """Test admin updating Event Manager credentials"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    with app.app_context():
        manager = User.query.filter_by(username='manager').first()
        manager_id = manager.id
    
    # Update Event Manager
    response = client.post(f'/admin/managers/{manager_id}/edit', data={
        'username': 'updatedmanager',
        'password': 'newpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify update
    with app.app_context():
        user = User.query.get(manager_id)
        assert user.username == 'updatedmanager'
        assert user.check_password('newpassword')

def test_admin_delete_event_manager(client, app):
    """Test admin deleting Event Manager account"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    with app.app_context():
        manager = User.query.filter_by(username='manager').first()
        manager_id = manager.id
    
    # Delete Event Manager
    response = client.post(f'/admin/managers/{manager_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify deletion
    with app.app_context():
        user = User.query.get(manager_id)
        assert user is None

def test_duplicate_username_prevention(client):
    """Test duplicate username prevention"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Try to create user with existing username
    response = client.post('/admin/managers/create', data={
        'username': 'manager',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert b'already exists' in response.data

def test_non_admin_access_denial(client):
    """Test non-admin access denial"""
    # Login as Event Manager
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    # Try to access admin route
    response = client.get('/admin/managers')
    assert response.status_code == 403

# Event Management Tests
def test_create_event_with_participants(client, app):
    """Test creating event with multiple participants"""
    # Login as manager
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster1 = Cluster.query.filter_by(name='Suryantra').first()
        cluster2 = Cluster.query.filter_by(name='Chandraloka').first()
    
    # Create event
    response = client.post('/events/create', data={
        'event_name': 'Test Event',
        'cluster_id[]': [cluster1.id, cluster2.id],
        'participant_name[]': ['Participant 1', 'Participant 2'],
        'position[]': [1, 2],
        'points[]': [10, 5]
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify event was created
    with app.app_context():
        event = Event.query.filter_by(name='Test Event').first()
        assert event is not None
        assert len(event.participants) == 2

def test_edit_event(client, app):
    """Test editing existing event"""
    # Login and create event first
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster = Cluster.query.first()
        manager = User.query.filter_by(username='manager').first()
        
        event = Event(name='Original Event', created_by=manager.id)
        db.session.add(event)
        db.session.commit()
        
        participant = Participant(
            event_id=event.id,
            cluster_id=cluster.id,
            name='Original Participant',
            position=1,
            points=10
        )
        db.session.add(participant)
        db.session.commit()
        
        event_id = event.id
    
    # Edit event
    response = client.post(f'/events/{event_id}/edit', data={
        'event_name': 'Updated Event',
        'cluster_id[]': [cluster.id],
        'participant_name[]': ['Updated Participant'],
        'position[]': [1],
        'points[]': [15]
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify update
    with app.app_context():
        event = Event.query.get(event_id)
        assert event.name == 'Updated Event'
        assert event.participants[0].points == 15

def test_delete_event(client, app):
    """Test deleting event"""
    # Login and create event first
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        manager = User.query.filter_by(username='manager').first()
        event = Event(name='Event to Delete', created_by=manager.id)
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    # Delete event
    response = client.post(f'/events/{event_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify deletion
    with app.app_context():
        event = Event.query.get(event_id)
        assert event is None

def test_view_event_details(client, app):
    """Test viewing event details"""
    # Login and create event
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster = Cluster.query.first()
        manager = User.query.filter_by(username='manager').first()
        
        event = Event(name='View Test Event', created_by=manager.id)
        db.session.add(event)
        db.session.commit()
        
        participant = Participant(
            event_id=event.id,
            cluster_id=cluster.id,
            name='Test Participant',
            position=1,
            points=10
        )
        db.session.add(participant)
        db.session.commit()
        
        event_id = event.id
    
    # View event
    response = client.get(f'/events/{event_id}')
    assert response.status_code == 200
    assert b'View Test Event' in response.data
    assert b'Test Participant' in response.data

# Overview Calculation Tests
def test_overview_point_aggregation(client, app):
    """Test correct point aggregation across events"""
    # Login
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster = Cluster.query.filter_by(name='Suryantra').first()
        manager = User.query.filter_by(username='manager').first()
        
        # Create multiple events
        event1 = Event(name='Event 1', created_by=manager.id)
        event2 = Event(name='Event 2', created_by=manager.id)
        db.session.add_all([event1, event2])
        db.session.commit()
        
        # Add participants
        p1 = Participant(event_id=event1.id, cluster_id=cluster.id, name='P1', position=1, points=10)
        p2 = Participant(event_id=event2.id, cluster_id=cluster.id, name='P2', position=1, points=15)
        db.session.add_all([p1, p2])
        db.session.commit()
    
    # View overview
    response = client.get('/overview')
    assert response.status_code == 200
    
    # Verify total points
    with app.app_context():
        cluster = Cluster.query.filter_by(name='Suryantra').first()
        assert cluster.get_total_points() == 25

def test_overview_cluster_sorting(client, app):
    """Test proper cluster sorting by total points"""
    # Login
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster1 = Cluster.query.filter_by(name='Suryantra').first()
        cluster2 = Cluster.query.filter_by(name='Chandraloka').first()
        manager = User.query.filter_by(username='manager').first()
        
        event = Event(name='Sorting Test', created_by=manager.id)
        db.session.add(event)
        db.session.commit()
        
        # Give cluster2 more points
        p1 = Participant(event_id=event.id, cluster_id=cluster1.id, name='P1', position=1, points=5)
        p2 = Participant(event_id=event.id, cluster_id=cluster2.id, name='P2', position=1, points=20)
        db.session.add_all([p1, p2])
        db.session.commit()
    
    # View overview
    response = client.get('/overview')
    assert response.status_code == 200
    
    # Verify Chandraloka appears before Suryantra (higher points)
    data = response.data.decode()
    chandraloka_pos = data.find('Chandraloka')
    suryantra_pos = data.find('Suryantra')
    assert chandraloka_pos < suryantra_pos

# Activity Logging Tests
def test_logs_created_for_operations(client, app):
    """Test logs created for all Event Manager operations"""
    # Login
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster = Cluster.query.first()
    
    # Create event (should log)
    client.post('/events/create', data={
        'event_name': 'Logged Event',
        'cluster_id[]': [cluster.id],
        'participant_name[]': ['Participant'],
        'position[]': [1],
        'points[]': [10]
    })
    
    # Verify log was created
    with app.app_context():
        log = ActivityLog.query.filter_by(action='create_event').first()
        assert log is not None
        assert 'Logged Event' in log.details

def test_log_entries_contain_correct_info(client, app):
    """Test log entries contain correct information"""
    # Login
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    with app.app_context():
        cluster = Cluster.query.first()
    
    # Create event
    client.post('/events/create', data={
        'event_name': 'Info Test Event',
        'cluster_id[]': [cluster.id],
        'participant_name[]': ['Test Participant'],
        'position[]': [1],
        'points[]': [10]
    })
    
    # Check log details
    with app.app_context():
        log = ActivityLog.query.filter_by(action='create_event').first()
        details = log.get_details_dict()
        assert details['event_name'] == 'Info Test Event'
        assert log.get_user().username == 'manager'

def test_admin_only_access_to_logs(client):
    """Test admin-only access to logs"""
    # Login as Event Manager
    client.post('/login', data={
        'username': 'manager',
        'password': 'manager123'
    })
    
    # Try to access logs
    response = client.get('/admin/logs')
    assert response.status_code == 403
    
    # Logout and login as admin
    client.get('/logout')
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Access logs
    response = client.get('/admin/logs')
    assert response.status_code == 200

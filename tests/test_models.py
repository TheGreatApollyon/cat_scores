import pytest
from models import User, Cluster, Event, Participant, ActivityLog, db
from app import create_app

@pytest.fixture
def app():
    """Create test application"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create database session"""
    with app.app_context():
        yield db.session

# User Model Tests
def test_user_password_hashing(db_session):
    """Test password hashing and verification"""
    user = User(username='testuser', role='event_manager')
    user.set_password('testpass123')
    
    assert user.password_hash is not None
    assert user.password_hash != 'testpass123'
    assert user.check_password('testpass123')
    assert not user.check_password('wrongpass')

def test_user_is_admin(db_session):
    """Test role checking methods"""
    admin = User(username='admin', role='admin')
    manager = User(username='manager', role='event_manager')
    
    assert admin.is_admin()
    assert not manager.is_admin()

def test_user_creation(db_session):
    """Test user creation and validation"""
    user = User(username='newuser', role='event_manager')
    user.set_password('password')
    
    db_session.add(user)
    db_session.commit()
    
    retrieved = User.query.filter_by(username='newuser').first()
    assert retrieved is not None
    assert retrieved.username == 'newuser'
    assert retrieved.role == 'event_manager'

# Cluster Model Tests
def test_cluster_total_points_calculation(db_session):
    """Test total points calculation"""
    cluster = Cluster(name='TestCluster')
    db_session.add(cluster)
    db_session.commit()
    
    user = User(username='testuser', role='event_manager')
    user.set_password('pass')
    db_session.add(user)
    db_session.commit()
    
    event = Event(name='Test Event', created_by=user.id)
    db_session.add(event)
    db_session.commit()
    
    # Add participants
    p1 = Participant(event_id=event.id, cluster_id=cluster.id, name='P1', position=1, points=10)
    p2 = Participant(event_id=event.id, cluster_id=cluster.id, name='P2', position=2, points=5)
    db_session.add_all([p1, p2])
    db_session.commit()
    
    assert cluster.get_total_points() == 15

def test_cluster_logo_url(db_session):
    """Test logo URL generation"""
    cluster = Cluster(name='TestCluster', logo_filename='test.png')
    assert cluster.get_logo_url() == '/static/images/clusters/test.png'
    
    cluster2 = Cluster(name='AnotherCluster')
    assert cluster2.get_logo_url() == '/static/images/clusters/anothercluster.png'

# Event and Participant Model Tests
def test_event_creation_with_participants(db_session):
    """Test event creation with participants"""
    user = User(username='creator', role='event_manager')
    user.set_password('pass')
    db_session.add(user)
    
    cluster = Cluster(name='Cluster1')
    db_session.add(cluster)
    db_session.commit()
    
    event = Event(name='Test Event', created_by=user.id)
    db_session.add(event)
    db_session.commit()
    
    participant = Participant(
        event_id=event.id,
        cluster_id=cluster.id,
        name='Participant 1',
        position=1,
        points=10
    )
    db_session.add(participant)
    db_session.commit()
    
    assert len(event.participants) == 1
    assert event.participants[0].name == 'Participant 1'

def test_participant_grouping_by_cluster(db_session):
    """Test participant grouping by cluster"""
    user = User(username='creator', role='event_manager')
    user.set_password('pass')
    db_session.add(user)
    
    cluster1 = Cluster(name='Cluster1')
    cluster2 = Cluster(name='Cluster2')
    db_session.add_all([cluster1, cluster2])
    db_session.commit()
    
    event = Event(name='Test Event', created_by=user.id)
    db_session.add(event)
    db_session.commit()
    
    p1 = Participant(event_id=event.id, cluster_id=cluster1.id, name='P1', position=1, points=10)
    p2 = Participant(event_id=event.id, cluster_id=cluster1.id, name='P2', position=2, points=5)
    p3 = Participant(event_id=event.id, cluster_id=cluster2.id, name='P3', position=1, points=8)
    db_session.add_all([p1, p2, p3])
    db_session.commit()
    
    grouped = event.get_participants_by_cluster()
    assert len(grouped) == 2
    assert 'Cluster1' in grouped
    assert 'Cluster2' in grouped
    assert len(grouped['Cluster1']['participants']) == 2
    assert len(grouped['Cluster2']['participants']) == 1

def test_participant_validation(db_session):
    """Test validation constraints"""
    user = User(username='creator', role='event_manager')
    user.set_password('pass')
    db_session.add(user)
    
    cluster = Cluster(name='Cluster1')
    db_session.add(cluster)
    db_session.commit()
    
    event = Event(name='Test Event', created_by=user.id)
    db_session.add(event)
    db_session.commit()
    
    # Test negative points
    with pytest.raises(ValueError):
        Participant(event_id=event.id, cluster_id=cluster.id, name='P1', position=1, points=-5)
    
    # Test invalid position
    with pytest.raises(ValueError):
        Participant(event_id=event.id, cluster_id=cluster.id, name='P1', position=0, points=10)

# ActivityLog Model Tests
def test_activity_log_creation(db_session):
    """Test log entry creation"""
    user = User(username='testuser', role='event_manager')
    user.set_password('pass')
    db_session.add(user)
    db_session.commit()
    
    log = ActivityLog(
        user_id=user.id,
        action='create_event',
        details='{"event_name": "Test Event"}'
    )
    db_session.add(log)
    db_session.commit()
    
    retrieved = ActivityLog.query.first()
    assert retrieved is not None
    assert retrieved.action == 'create_event'
    assert retrieved.get_user().username == 'testuser'

def test_activity_log_details_parsing(db_session):
    """Test log detail formatting"""
    user = User(username='testuser', role='event_manager')
    user.set_password('pass')
    db_session.add(user)
    db_session.commit()
    
    log = ActivityLog(
        user_id=user.id,
        action='edit_event',
        details='{"event_name": "Updated Event", "old_name": "Old Event"}'
    )
    db_session.add(log)
    db_session.commit()
    
    details = log.get_details_dict()
    assert details['event_name'] == 'Updated Event'
    assert details['old_name'] == 'Old Event'

from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User, Cluster
from utils.decorators import login_required
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Ensure instance folder exists
    os.makedirs('instance', exist_ok=True)
    
    # Initialize database
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
    
    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return "403 - Forbidden: You don't have permission to access this page", 403
    
    @app.errorhandler(404)
    def not_found(e):
        return "404 - Not Found: The requested resource was not found", 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return "500 - Internal Server Error: Something went wrong", 500
    
    # Root route - public leaderboard
    @app.route('/')
    def index():
        return redirect(url_for('overview.public_overview'))
    
    # Legacy /overview route - redirect to /leaderboard
    @app.route('/overview')
    def overview_redirect():
        return redirect(url_for('overview.public_overview'))
    
    # Manage route - requires login
    @app.route('/manage')
    @login_required
    def manage():
        return redirect(url_for('overview.manage_overview'))
    
    # Initialize database
    with app.app_context():
        db.create_all()
        init_database()
    
    return app

def init_database():
    """Initialize database with default data"""
    from models import User, Cluster, Event, Participant
    
    # Check if clusters already exist
    if Cluster.query.count() == 0:
        # Create 7 predefined clusters
        clusters = [
            Cluster(name='Suryantra', logo_filename='suryantra.png'),
            Cluster(name='Chandraloka', logo_filename='chandraloka.png'),
            Cluster(name='Swarnika', logo_filename='swarnika.png'),
            Cluster(name='Ushnavi', logo_filename='ushnavi.png'),
            Cluster(name='Taraksha', logo_filename='taraksha.png'),
            Cluster(name='Maya', logo_filename='maya.png'),
            Cluster(name='Meghora', logo_filename='meghora.png')
        ]
        for cluster in clusters:
            db.session.add(cluster)
        db.session.commit()
        print("✓ Created 7 predefined clusters")
    
    # Check if admin account exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Created default admin account (username: admin, password: admin123)")
        print("⚠ IMPORTANT: Change the admin password after first login!")
    
    # Create a test event if no events exist
    if Event.query.count() == 0:
        admin = User.query.filter_by(username='admin').first()
        if admin:
            test_event = Event(name='Sample Competition - Opening Ceremony', created_by=admin.id)
            db.session.add(test_event)
            db.session.flush()
            
            # Add sample participants from different clusters
            clusters = Cluster.query.all()
            if len(clusters) >= 3:
                participants = [
                    Participant(event_id=test_event.id, cluster_id=clusters[0].id, 
                               name='Team Alpha', position=1, points=100),
                    Participant(event_id=test_event.id, cluster_id=clusters[1].id, 
                               name='Team Beta', position=2, points=85),
                    Participant(event_id=test_event.id, cluster_id=clusters[2].id, 
                               name='Team Gamma', position=3, points=70),
                    Participant(event_id=test_event.id, cluster_id=clusters[0].id, 
                               name='Team Delta', position=4, points=60),
                ]
                for participant in participants:
                    db.session.add(participant)
                
                db.session.commit()
                print("✓ Created sample test event with participants")

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print("Event Scoring System")
    print("="*50)
    print("Server starting at http://127.0.0.1:5000")
    print("Default admin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)

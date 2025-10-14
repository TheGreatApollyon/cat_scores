from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User, Cluster
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
    
    # Root route - public overview
    @app.route('/')
    def index():
        return redirect(url_for('overview.public_overview'))
    
    # Initialize database
    with app.app_context():
        db.create_all()
        init_database()
    
    return app

def init_database():
    """Initialize database with default data"""
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

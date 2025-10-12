from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Configure for production or development
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production'

if IS_PRODUCTION:
    # Cache static files for 1 year in production
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
else:
    # Disable caching in development
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'catLogo.png',
        mimetype='image/png'
    )

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return "Internal Server Error", 500

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5001)

# Production Deployment Guide

## Gunicorn Deployment

The app is now configured to work with Gunicorn for production deployment.

### Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Gunicorn:**

   ```bash
   # Option 1: Simple command
   gunicorn app:app --bind 0.0.0.0:80

   # Option 2: With configuration file
   gunicorn --config gunicorn.conf.py app:app

   # Option 3: Use the startup script
   ./start-production.sh
   ```

### Configuration Options

#### Basic Gunicorn Command

```bash
gunicorn app:app \
  --bind 0.0.0.0:80 \
  --workers 4 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile -
```

#### Using Configuration File

The included `gunicorn.conf.py` provides production-ready settings:

- Automatic worker scaling based on CPU cores
- Request limits to prevent memory leaks
- Proper logging configuration
- Optimized timeouts and connections

### Environment Variables

Create a `.env` file for production:

```bash
SECRET_KEY=your-super-secret-production-key-here
DATABASE_URL=sqlite:///event_scoring.db
FLASK_ENV=production
```

### File Structure for Deployment

```
event-scoring-system/
├── app.py                 # Main Flask app (contains 'app' variable)
├── wsgi.py               # WSGI entry point (alternative)
├── gunicorn.conf.py      # Gunicorn configuration
├── start-production.sh   # Startup script
├── requirements.txt      # Dependencies (includes gunicorn)
├── .env                  # Environment variables (create this)
└── ... (rest of the files)
```

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
```

### Nginx Reverse Proxy (Recommended)

If using Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Troubleshooting

#### Common Issues

1. **"Failed to find attribute 'app' in 'app'"**

   - ✅ **FIXED**: The app now has a global `app` variable
   - Use: `gunicorn app:app`

2. **Permission denied on port 80**

   - Run as root: `sudo gunicorn app:app --bind 0.0.0.0:80`
   - Or use a different port: `gunicorn app:app --bind 0.0.0.0:8000`

3. **Database not found**

   - Ensure the `instance/` directory exists
   - Check file permissions
   - The app will create the database automatically

4. **Static files not loading**
   - Ensure static files are included in deployment
   - Use Nginx to serve static files in production
   - Check file paths in templates

### Health Check

Test that the app is running:

```bash
curl http://localhost/leaderboard
```

### Monitoring

For production monitoring, consider:

- Process managers like `systemd` or `supervisor`
- Log aggregation tools
- Health check endpoints
- Performance monitoring

### Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Configure firewall rules
- [ ] Regular database backups
- [ ] Update dependencies regularly

## Default Credentials

**⚠️ IMPORTANT**: Change these immediately after deployment!

- Username: `admin`
- Password: `admin123`

## Support

The app includes:

- ✅ Auto-database creation
- ✅ Sample data seeding
- ✅ Error handling
- ✅ Real-time updates
- ✅ Mobile responsive design
- ✅ Production-ready configuration

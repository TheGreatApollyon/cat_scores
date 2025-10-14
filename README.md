# Event Scoring System

A Flask-based web application for managing competitive events across 7 predefined clusters. The system provides role-based access control with Admin and Event Manager roles, allowing authorized users to create events, assign scores to participants from different clusters, and view aggregated cluster standings.

## Features

- **Role-Based Access Control**: Admin and Event Manager roles with different permissions
- **Event Management**: Create, edit, and delete events with multiple participants
- **Cluster Leaderboard**: Real-time overview of total points per cluster
- **Activity Logging**: Comprehensive audit trail of all operations
- **User Management**: Admin can create and manage Event Manager accounts
- **Local Deployment**: Runs entirely locally using SQLite database

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the repository**

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

4. **Default Admin Credentials**

On first run, a default admin account is created:

- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANT**: Change the admin password after first login!

## Public Access

The cluster leaderboard is **publicly accessible** at the root URL without requiring login:

- **Public Leaderboard**: http://127.0.0.1:5000/
  - View real-time cluster standings
  - See total points for all clusters
  - No authentication required

## Management Access

All management functions require login and are accessible at `/manage`:

- **Management Dashboard**: http://127.0.0.1:5000/manage
- **Login Page**: http://127.0.0.1:5000/login

### Admin Role

Admins have full access to all management features:

1. **Event Manager Management**

   - Navigate to "Event Managers" in the menu
   - Create new Event Manager accounts with username and password
   - Edit existing Event Manager credentials
   - Delete Event Manager accounts

2. **Event Management**

   - Create, edit, and delete events
   - Add multiple participants from different clusters
   - Assign positions and points to participants

3. **View Overview**

   - See cluster leaderboard with total points
   - Clusters are sorted by total points in descending order

4. **Activity Logs**
   - View all operations performed by Event Managers
   - See timestamps, usernames, and operation details

### Event Manager Role

Event Managers can:

1. **Create Events**

   - Navigate to "Events" → "Create New Event"
   - Enter event name
   - Add participants by selecting cluster, entering name, position, and points
   - Click "Add Participant" to add more participants
   - Submit to create the event

2. **Edit Events**

   - Click "Edit" on any event
   - Modify event name and participant details
   - Add or remove participants

3. **Delete Events**

   - Click "Delete" on any event
   - Confirm deletion

4. **View Overview**
   - See cluster leaderboard with total points

## Cluster Configuration

The system comes with 7 predefined clusters:

1. Suryantra
2. Chandraloka
3. Swarnika
4. Ushnavi
5. Taraksha
6. Maya
7. Meghora

### Replacing Cluster Logos

To replace cluster logos with your own images:

1. Navigate to `static/images/clusters/`
2. Replace the placeholder files with your logo images
3. Use PNG format for best results
4. Name files as: `clustername.png` (e.g., `suryantra.png`)
5. Recommended size: 200x200 pixels or similar square dimensions

## Running Tests

The application includes comprehensive unit and integration tests.

### Install test dependencies

```bash
pip install pytest
```

### Run all tests

```bash
pytest tests/
```

### Run specific test files

```bash
pytest tests/test_models.py
pytest tests/test_integration.py
```

## Database

The application uses SQLite for data persistence. The database file is located at:

```
instance/event_scoring.db
```

### Database Backup

To backup the database, simply copy the database file:

```bash
cp instance/event_scoring.db instance/event_scoring_backup_$(date +%Y%m%d_%H%M%S).db
```

Or use the provided backup script:

```bash
python backup_db.py
```

## Configuration

Configuration settings are in `config.py`. You can customize:

- Secret key for session management
- Database URI
- Session timeout
- CSRF protection settings

### Environment Variables

Create a `.env` file (see `.env.example`) to override default settings:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/event_scoring.db
```

## Security Features

- Password hashing using PBKDF2-SHA256
- CSRF protection on all forms
- Session-based authentication
- Role-based access control
- SQL injection prevention via SQLAlchemy ORM
- Input validation and sanitization

## Troubleshooting

### Application won't start

- Ensure Python 3.8+ is installed: `python --version`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is available

### Can't log in

- Verify you're using the correct credentials
- Default admin: username `admin`, password `admin123`
- Check if database file exists in `instance/` folder

### Database errors

- Delete the database file and restart the application to recreate it
- Ensure the `instance/` directory exists and is writable

### Cluster logos not displaying

- Verify image files exist in `static/images/clusters/`
- Check file names match cluster names (lowercase)
- Ensure images are in PNG format
- Clear browser cache

### Tests failing

- Ensure pytest is installed: `pip install pytest`
- Run tests from the project root directory
- Check that all dependencies are installed

## Project Structure

```
event-scoring-system/
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── routes/                     # Route handlers
│   ├── auth.py                 # Authentication routes
│   ├── admin.py                # Admin routes
│   ├── events.py               # Event management routes
│   ├── overview.py             # Overview/leaderboard routes
│   └── logs.py                 # Activity log routes
├── utils/                      # Utility modules
│   ├── decorators.py           # Authentication decorators
│   └── logger.py               # Activity logging
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── login.html              # Login page
│   ├── overview.html           # Cluster leaderboard
│   ├── admin/                  # Admin templates
│   └── events/                 # Event templates
├── static/                     # Static assets
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/clusters/        # Cluster logos
├── tests/                      # Test files
│   ├── test_models.py          # Unit tests
│   └── test_integration.py     # Integration tests
└── instance/                   # Instance folder (created on first run)
    └── event_scoring.db        # SQLite database
```

## License

This project is provided as-is for educational and internal use.

## Support

For issues or questions, please refer to the troubleshooting section above or contact your system administrator.

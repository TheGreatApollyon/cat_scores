# Design Document

## Overview

The Event Scoring System is a Flask-based web application that manages competitive events across 7 predefined clusters. The application follows the Model-View-Controller (MVC) pattern with Flask serving as the web framework, SQLite for data persistence, and a combination of server-side rendering (Jinja2 templates) and client-side JavaScript for the user interface.

The system architecture emphasizes simplicity, local deployment, and clear separation of concerns. Authentication is handled through Flask sessions, with role-based access control implemented via decorators. The application is designed to run entirely locally without external dependencies beyond Python packages.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     HTML     │  │     CSS      │  │  JavaScript  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP Requests/Responses
                            │
┌─────────────────────────────────────────────────────────────┐
│                      Flask Application                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Routes Layer                       │   │
│  │  (auth, admin, events, overview, logs)               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Business Logic                       │   │
│  │  (authentication, authorization, event management)   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Data Access Layer                   │   │
│  │  (SQLAlchemy ORM models and queries)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                    Database Operations
                            │
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  (users, clusters, events, participants, logs)              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend Framework**: Flask 3.x
- **Database**: SQLite 3 with SQLAlchemy ORM
- **Template Engine**: Jinja2 (included with Flask)
- **Authentication**: Flask-Login for session management
- **Password Hashing**: Werkzeug security utilities
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Static Assets**: Flask static file serving

### Directory Structure

```
event-scoring-system/
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── models.py                   # SQLAlchemy database models
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Authentication routes
│   ├── admin.py                # Admin-only routes
│   ├── events.py               # Event management routes
│   ├── overview.py             # Overview/leaderboard routes
│   └── logs.py                 # Activity log routes
├── utils/
│   ├── __init__.py
│   ├── decorators.py           # Custom decorators (role checks)
│   └── logger.py               # Activity logging utilities
├── static/
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   ├── js/
│   │   ├── events.js           # Event management JavaScript
│   │   └── overview.js         # Overview page JavaScript
│   └── images/
│       └── clusters/           # Cluster logo images
│           ├── suryantra.png
│           ├── chandraloka.png
│           ├── swarnika.png
│           ├── ushnavi.png
│           ├── taraksha.png
│           ├── maya.png
│           └── meghora.png
├── templates/
│   ├── base.html               # Base template with navigation
│   ├── login.html              # Login page
│   ├── admin/
│   │   ├── managers.html       # Event Manager management
│   │   └── logs.html           # Activity logs view
│   ├── events/
│   │   ├── list.html           # Event list view
│   │   ├── create.html         # Event creation form
│   │   ├── edit.html           # Event editing form
│   │   └── view.html           # Single event view
│   └── overview.html           # Cluster leaderboard
└── instance/
    └── event_scoring.db        # SQLite database file
```

## Components and Interfaces

### 1. Authentication System

**Component**: `routes/auth.py` + `utils/decorators.py`

**Responsibilities**:

- Handle user login and logout
- Manage Flask sessions
- Provide role-based access control decorators

**Key Functions**:

- `login()`: Authenticate user credentials and create session
- `logout()`: Terminate user session
- `@login_required`: Decorator to protect routes requiring authentication
- `@admin_required`: Decorator to protect admin-only routes

**Session Data**:

```python
session = {
    'user_id': int,
    'username': str,
    'role': str  # 'admin' or 'event_manager'
}
```

### 2. User Management

**Component**: `routes/admin.py`

**Responsibilities**:

- CRUD operations for Event Manager accounts
- Admin-only functionality

**Key Endpoints**:

- `GET /admin/managers`: List all Event Managers
- `POST /admin/managers/create`: Create new Event Manager
- `POST /admin/managers/<id>/edit`: Update Event Manager
- `POST /admin/managers/<id>/delete`: Delete Event Manager

### 3. Event Management

**Component**: `routes/events.py`

**Responsibilities**:

- Create, read, update, delete events
- Manage event participants and scores
- Handle multi-participant, multi-position events

**Key Endpoints**:

- `GET /events`: List all events
- `GET /events/create`: Display event creation form
- `POST /events/create`: Process event creation
- `GET /events/<id>`: View single event details
- `GET /events/<id>/edit`: Display event editing form
- `POST /events/<id>/edit`: Process event updates
- `POST /events/<id>/delete`: Delete event

**Event Creation Flow**:

1. User submits event name
2. User adds participants dynamically (cluster, name, position, points)
3. System validates all inputs
4. System creates event and participant records
5. System logs the operation
6. System redirects to event list with success message

### 4. Overview Dashboard

**Component**: `routes/overview.py`

**Responsibilities**:

- Calculate total points per cluster
- Display cluster leaderboard
- Aggregate data from all events

**Key Endpoint**:

- `GET /overview`: Display cluster leaderboard

**Calculation Logic**:

```python
# For each cluster:
total_points = SUM(participants.points WHERE participants.cluster_id == cluster.id)
# Sort clusters by total_points DESC
```

### 5. Activity Logging

**Component**: `utils/logger.py`

**Responsibilities**:

- Log all Event Manager operations
- Provide audit trail functionality

**Logged Operations**:

- Event creation (event_name, timestamp, user)
- Event modification (event_name, changes, timestamp, user)
- Event deletion (event_name, timestamp, user)

**Log Entry Format**:

```python
{
    'timestamp': datetime,
    'user_id': int,
    'username': str,
    'action': str,  # 'create_event', 'edit_event', 'delete_event'
    'details': str  # JSON string with operation details
}
```

### 6. Static Asset Management

**Component**: Flask static file serving

**Responsibilities**:

- Serve CSS, JavaScript, and image files
- Provide cluster logos for display

**Cluster Logo Convention**:

- Filename format: `{cluster_name_lowercase}.png`
- Location: `static/images/clusters/`
- Fallback: Display cluster name if logo not found

## Data Models

### User Model

```python
class User(db.Model):
    id = Integer, Primary Key, Auto-increment
    username = String(80), Unique, Not Null
    password_hash = String(255), Not Null
    role = String(20), Not Null  # 'admin' or 'event_manager'
    created_at = DateTime, Default=now()

    # Methods
    def set_password(password): # Hash and store password
    def check_password(password): # Verify password
    def is_admin(): # Check if user is admin
```

**Relationships**:

- One-to-many with ActivityLog (user creates many logs)

### Cluster Model

```python
class Cluster(db.Model):
    id = Integer, Primary Key, Auto-increment
    name = String(50), Unique, Not Null
    logo_filename = String(100), Nullable
    created_at = DateTime, Default=now()

    # Methods
    def get_total_points(): # Calculate sum of all participant points
    def get_logo_url(): # Return URL to logo image
```

**Predefined Clusters**:

1. Suryantra
2. Chandraloka
3. Swarnika
4. Ushnavi
5. Taraksha
6. Maya
7. Meghora

**Relationships**:

- One-to-many with Participant (cluster has many participants)

### Event Model

```python
class Event(db.Model):
    id = Integer, Primary Key, Auto-increment
    name = String(200), Not Null
    created_by = Integer, Foreign Key(User.id), Not Null
    created_at = DateTime, Default=now()
    updated_at = DateTime, OnUpdate=now()

    # Methods
    def get_participants_by_cluster(): # Group participants by cluster
    def get_creator(): # Return User object who created event
```

**Relationships**:

- Many-to-one with User (event created by one user)
- One-to-many with Participant (event has many participants)

### Participant Model

```python
class Participant(db.Model):
    id = Integer, Primary Key, Auto-increment
    event_id = Integer, Foreign Key(Event.id), Not Null
    cluster_id = Integer, Foreign Key(Cluster.id), Not Null
    name = String(100), Not Null
    position = Integer, Not Null  # 1 for 1st place, 2 for 2nd, etc.
    points = Integer, Not Null
    created_at = DateTime, Default=now()
```

**Relationships**:

- Many-to-one with Event (participant belongs to one event)
- Many-to-one with Cluster (participant belongs to one cluster)

**Constraints**:

- points >= 0
- position >= 1

### ActivityLog Model

```python
class ActivityLog(db.Model):
    id = Integer, Primary Key, Auto-increment
    user_id = Integer, Foreign Key(User.id), Not Null
    action = String(50), Not Null  # 'create_event', 'edit_event', 'delete_event'
    details = Text, Nullable  # JSON string with additional information
    timestamp = DateTime, Default=now()

    # Methods
    def get_user(): # Return User object
    def get_details_dict(): # Parse JSON details to dictionary
```

**Relationships**:

- Many-to-one with User (log entry created by one user)

### Database Relationships Diagram

```
User (1) ──────────── (*) Event
  │                        │
  │                        │
  │                        │
  └─── (*) ActivityLog     └─── (*) Participant
                                      │
                                      │
                                      │
                            Cluster (1) ───────
```

## Error Handling

### Authentication Errors

**Scenario**: Invalid login credentials

- **Response**: Flash error message "Invalid username or password"
- **Action**: Remain on login page with form cleared

**Scenario**: Unauthorized access attempt

- **Response**: Redirect to login page with flash message "Please log in to access this page"
- **Action**: Store intended URL for post-login redirect

**Scenario**: Insufficient permissions (Event Manager accessing admin routes)

- **Response**: HTTP 403 Forbidden with error page
- **Action**: Display message "You don't have permission to access this page"

### Data Validation Errors

**Scenario**: Duplicate username during Event Manager creation

- **Response**: Flash error message "Username already exists"
- **Action**: Return to form with existing data preserved

**Scenario**: Missing required fields in event creation

- **Response**: Flash error message listing missing fields
- **Action**: Return to form with existing data preserved

**Scenario**: Invalid point values (negative numbers)

- **Response**: Flash error message "Points must be positive numbers"
- **Action**: Return to form with existing data preserved

**Scenario**: Invalid cluster selection

- **Response**: Flash error message "Invalid cluster selected"
- **Action**: Return to form with existing data preserved

### Database Errors

**Scenario**: Database connection failure

- **Response**: HTTP 500 Internal Server Error
- **Action**: Log error details, display generic error page to user

**Scenario**: Constraint violation (foreign key, unique)

- **Response**: Flash error message with user-friendly explanation
- **Action**: Rollback transaction, return to previous page

**Scenario**: Record not found (accessing non-existent event)

- **Response**: HTTP 404 Not Found
- **Action**: Display "Event not found" page with link to event list

### File Upload Errors (Cluster Logos)

**Scenario**: Missing cluster logo file

- **Response**: Display cluster name as text fallback
- **Action**: Continue rendering page without error

**Scenario**: Invalid image format

- **Response**: Flash error message "Invalid image format. Please upload PNG, JPG, or GIF"
- **Action**: Return to form

## Testing Strategy

### Unit Tests

**Target**: Individual functions and methods

**Test Cases**:

1. **User Model**

   - Password hashing and verification
   - Role checking methods
   - User creation and validation

2. **Cluster Model**

   - Total points calculation
   - Logo URL generation

3. **Event Model**

   - Participant grouping by cluster
   - Event creation and updates

4. **Activity Logger**
   - Log entry creation
   - Log detail formatting

**Tools**: pytest, Flask test client

### Integration Tests

**Target**: Route handlers and database interactions

**Test Cases**:

1. **Authentication Flow**

   - Successful login with valid credentials
   - Failed login with invalid credentials
   - Session persistence across requests
   - Logout functionality

2. **Event Manager CRUD**

   - Admin creates Event Manager account
   - Admin updates Event Manager credentials
   - Admin deletes Event Manager account
   - Duplicate username prevention

3. **Event Management**

   - Create event with multiple participants
   - Edit existing event
   - Delete event
   - View event details

4. **Overview Calculation**

   - Correct point aggregation across events
   - Proper cluster sorting by total points

5. **Activity Logging**
   - Logs created for all Event Manager operations
   - Log entries contain correct information

**Tools**: pytest, Flask test client, temporary SQLite database

### Functional Tests

**Target**: End-to-end user workflows

**Test Scenarios**:

1. **Admin Workflow**

   - Login as admin
   - Create Event Manager account
   - Create event with participants
   - View overview dashboard
   - Check activity logs
   - Logout

2. **Event Manager Workflow**

   - Login as Event Manager
   - Create event with multiple clusters
   - Add multiple participants from same cluster
   - Edit event to update points
   - View overview dashboard
   - Logout

3. **Multi-User Scenario**
   - Multiple Event Managers create events simultaneously
   - Verify point calculations remain accurate
   - Verify logs attribute actions to correct users

**Tools**: Selenium WebDriver or Playwright for browser automation

### Security Tests

**Test Cases**:

1. **Authentication Bypass Attempts**

   - Access protected routes without login
   - Access admin routes as Event Manager
   - Session hijacking prevention

2. **SQL Injection Prevention**

   - Test all input fields with SQL injection payloads
   - Verify SQLAlchemy ORM prevents injection

3. **Password Security**

   - Verify passwords are hashed in database
   - Verify password hashes use strong algorithm (bcrypt/pbkdf2)

4. **CSRF Protection**
   - Verify forms include CSRF tokens
   - Verify POST requests validate CSRF tokens

**Tools**: OWASP ZAP, manual testing

### Performance Tests

**Test Cases**:

1. **Database Query Efficiency**

   - Measure query time for overview calculation with 100+ events
   - Verify proper indexing on foreign keys

2. **Page Load Times**

   - Measure load time for event list with 50+ events
   - Measure load time for overview page

3. **Concurrent User Handling**
   - Simulate 10 concurrent users creating events
   - Verify no data corruption or race conditions

**Tools**: pytest-benchmark, locust for load testing

### Test Data Setup

**Initial Database State**:

- 1 Admin account (username: admin, password: admin123)
- 7 Cluster records (predefined clusters)
- 2 Event Manager accounts for testing
- 5 sample events with participants
- Activity logs for sample operations

**Test Fixtures**:

- `app_fixture`: Flask application with test configuration
- `db_fixture`: Temporary SQLite database
- `client_fixture`: Flask test client
- `auth_fixture`: Authenticated sessions (admin and event_manager)

### Continuous Testing

**Pre-commit Hooks**:

- Run unit tests before allowing commits
- Check code formatting (black, flake8)

**CI/CD Pipeline** (if applicable):

- Run full test suite on push
- Generate coverage reports
- Fail build if coverage < 80%

## Implementation Notes

### Initial Setup

1. **Database Initialization**:

   - Create all tables on first run
   - Seed 7 predefined clusters
   - Create default admin account (username: admin, password: admin123)
   - Prompt to change admin password on first login

2. **Static Assets**:

   - Include placeholder cluster logos in repository
   - Provide instructions for replacing with actual logos

3. **Configuration**:
   - Use environment variables for sensitive settings
   - Provide `.env.example` file with required variables
   - Default to development mode with debug enabled

### Security Considerations

1. **Password Hashing**: Use Werkzeug's `generate_password_hash()` with method='pbkdf2:sha256'
2. **Session Security**: Set secure session cookie flags in production
3. **CSRF Protection**: Use Flask-WTF for form CSRF tokens
4. **Input Validation**: Validate and sanitize all user inputs
5. **SQL Injection**: Use SQLAlchemy ORM exclusively (no raw SQL)

### UI/UX Design Principles

1. **Responsive Design**: Mobile-friendly layout using CSS flexbox/grid
2. **Accessibility**: Proper semantic HTML, ARIA labels, keyboard navigation
3. **Visual Feedback**: Loading spinners, success/error messages, form validation
4. **Consistent Styling**: Unified color scheme, typography, spacing
5. **Intuitive Navigation**: Clear menu structure, breadcrumbs, back buttons

### Performance Optimizations

1. **Database Indexing**: Index foreign keys and frequently queried columns
2. **Query Optimization**: Use eager loading for relationships to avoid N+1 queries
3. **Caching**: Cache cluster total calculations (invalidate on event changes)
4. **Static Asset Compression**: Minify CSS/JS in production
5. **Database Connection Pooling**: Use SQLAlchemy connection pooling

### Deployment Considerations

1. **Single-File Deployment**: Package application as standalone executable (PyInstaller)
2. **Database Backup**: Provide script to backup SQLite database
3. **Log Rotation**: Implement log file rotation to prevent disk space issues
4. **Error Monitoring**: Log all errors to file for debugging
5. **Documentation**: Include README with setup and usage instructions

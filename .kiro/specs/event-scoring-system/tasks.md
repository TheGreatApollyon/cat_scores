# Implementation Plan

- [x] 1. Set up project structure and dependencies

  - Create project directory structure (routes/, utils/, templates/, static/)
  - Create requirements.txt with Flask, SQLAlchemy, Flask-Login dependencies
  - Create config.py with application configuration settings
  - _Requirements: 8.5_

- [x] 2. Implement database models

  - [x] 2.1 Create User model with authentication methods

    - Implement User class with id, username, password_hash, role, created_at fields
    - Add set_password() method using Werkzeug password hashing
    - Add check_password() method for authentication
    - Add is_admin() method for role checking
    - _Requirements: 1.2, 1.3, 2.2, 2.3, 10.1, 10.2_

  - [x] 2.2 Create Cluster model

    - Implement Cluster class with id, name, logo_filename, created_at fields
    - Add get_total_points() method to calculate sum of participant points
    - Add get_logo_url() method to return static file URL
    - _Requirements: 3.1, 3.2, 3.3, 6.2_

  - [x] 2.3 Create Event model

    - Implement Event class with id, name, created_by, created_at, updated_at fields
    - Add relationship to User model
    - Add get_participants_by_cluster() method to group participants
    - Add get_creator() method to return User object
    - _Requirements: 4.1, 4.5, 4.6_

  - [x] 2.4 Create Participant model

    - Implement Participant class with id, event_id, cluster_id, name, position, points fields
    - Add relationships to Event and Cluster models
    - Add validation for points >= 0 and position >= 1
    - _Requirements: 4.2, 4.3, 4.4, 5.3, 5.5_

  - [x] 2.5 Create ActivityLog model
    - Implement ActivityLog class with id, user_id, action, details, timestamp fields
    - Add relationship to User model
    - Add get_user() method
    - Add get_details_dict() method to parse JSON details
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.6_

- [x] 3. Create utility modules

  - [x] 3.1 Implement authentication decorators

    - Create utils/decorators.py file
    - Implement @login_required decorator to protect authenticated routes
    - Implement @admin_required decorator to protect admin-only routes
    - _Requirements: 1.6, 2.1_

  - [x] 3.2 Implement activity logging utilities
    - Create utils/logger.py file
    - Implement log_activity() function to create ActivityLog entries
    - Support logging for create_event, edit_event, delete_event actions
    - _Requirements: 7.1, 7.2, 7.3, 7.6_

- [x] 4. Implement authentication routes

  - [x] 4.1 Create login functionality

    - Create routes/auth.py file
    - Implement GET /login route to display login form
    - Implement POST /login route to authenticate users
    - Set up Flask session with user_id, username, role
    - _Requirements: 1.1, 1.2, 1.4_

  - [x] 4.2 Create logout functionality

    - Implement /logout route to clear session
    - Redirect to login page after logout
    - _Requirements: 1.5_

  - [x] 4.3 Create login template
    - Create templates/login.html with username and password fields
    - Add form validation and error message display
    - _Requirements: 1.1, 1.3, 9.5_

- [x] 5. Implement admin routes for Event Manager management

  - [x] 5.1 Create Event Manager list view

    - Create routes/admin.py file
    - Implement GET /admin/managers route with @admin_required decorator
    - Query and display all Event Manager accounts
    - _Requirements: 2.1, 2.4_

  - [x] 5.2 Create Event Manager creation functionality

    - Implement POST /admin/managers/create route
    - Validate unique username and required fields
    - Hash password and create User record with role='event_manager'
    - _Requirements: 2.2, 2.3, 2.7_

  - [x] 5.3 Create Event Manager edit functionality

    - Implement POST /admin/managers/<id>/edit route
    - Allow updating username and password
    - Validate and update User record
    - _Requirements: 2.6_

  - [x] 5.4 Create Event Manager delete functionality

    - Implement POST /admin/managers/<id>/delete route
    - Remove User record from database
    - _Requirements: 2.5_

  - [x] 5.5 Create Event Manager management template
    - Create templates/admin/managers.html
    - Display list of Event Managers with edit/delete buttons
    - Include form for creating new Event Manager
    - _Requirements: 2.1, 2.4, 9.2, 9.5_

- [x] 6. Implement event management routes

  - [x] 6.1 Create event list view

    - Create routes/events.py file
    - Implement GET /events route to display all events
    - Query Event model and render list
    - _Requirements: 4.6_

  - [x] 6.2 Create event creation functionality

    - Implement GET /events/create route to display form
    - Implement POST /events/create route to process submission
    - Support adding multiple participants with cluster, name, position, points
    - Create Event and Participant records
    - Log activity using log_activity()
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 7.1_

  - [x] 6.3 Create event view functionality

    - Implement GET /events/<id> route to display single event
    - Group participants by cluster using get_participants_by_cluster()
    - Display event name, cluster logos, and participant details
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [x] 6.4 Create event edit functionality

    - Implement GET /events/<id>/edit route to display edit form
    - Implement POST /events/<id>/edit route to process updates
    - Allow modification of event name and all participant data
    - Log activity with modified details
    - _Requirements: 4.7, 7.2_

  - [x] 6.5 Create event delete functionality

    - Implement POST /events/<id>/delete route
    - Remove Event and associated Participant records
    - Log activity with deleted event name
    - _Requirements: 4.8, 7.3_

  - [x] 6.6 Create event templates
    - Create templates/events/list.html for event list
    - Create templates/events/create.html for event creation form with dynamic participant addition
    - Create templates/events/view.html for single event display with cluster logos
    - Create templates/events/edit.html for event editing
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 9.4, 9.5_

- [x] 7. Implement overview/leaderboard functionality

  - [x] 7.1 Create overview route

    - Create routes/overview.py file
    - Implement GET /overview route
    - Calculate total points per cluster using get_total_points()
    - Sort clusters by total points in descending order
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [x] 7.2 Create overview template
    - Create templates/overview.html
    - Display cluster leaderboard with logos, names, and total points
    - Sort by points descending
    - _Requirements: 6.1, 6.3, 6.4_

- [x] 8. Implement activity log functionality

  - [x] 8.1 Create logs route

    - Create routes/logs.py file
    - Implement GET /admin/logs route with @admin_required decorator
    - Query ActivityLog entries in chronological order
    - _Requirements: 7.4, 7.5_

  - [x] 8.2 Create logs template
    - Create templates/admin/logs.html
    - Display username, action type, timestamp, and details for each log entry
    - _Requirements: 7.5_

- [x] 9. Create base template and navigation

  - [x] 9.1 Create base template

    - Create templates/base.html with common layout
    - Include navigation menu that changes based on user role
    - Add blocks for page title and content
    - _Requirements: 9.1, 9.4_

  - [x] 9.2 Implement role-based navigation
    - Show Overview, Events, Event Manager Management, Logs for Admin
    - Show Overview, Events for Event Manager
    - Include logout button
    - _Requirements: 9.2, 9.3_

- [x] 10. Create static assets

  - [x] 10.1 Create CSS stylesheet

    - Create static/css/style.css
    - Implement responsive design with flexbox/grid
    - Style forms, tables, navigation, buttons
    - Ensure consistent color scheme and typography
    - _Requirements: 9.4_

  - [x] 10.2 Create JavaScript for dynamic forms

    - Create static/js/events.js
    - Implement dynamic participant addition/removal in event forms
    - Add client-side form validation
    - _Requirements: 4.2, 4.3, 4.4, 9.5_

  - [x] 10.3 Add cluster logo placeholders
    - Create static/images/clusters/ directory
    - Add placeholder images for all 7 clusters (suryantra.png, chandraloka.png, etc.)
    - _Requirements: 3.2, 5.2, 5.6_

- [x] 11. Create main application file

  - [x] 11.1 Implement app.py

    - Create Flask application instance
    - Configure SQLAlchemy with SQLite database
    - Set up Flask-Login
    - Register all blueprints (auth, admin, events, overview, logs)
    - Add error handlers for 403, 404, 500
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [x] 11.2 Implement database initialization
    - Create database tables on first run
    - Seed 7 predefined clusters (Suryantra, Chandraloka, Swarnika, Ushnavi, Taraksha, Maya, Meghora)
    - Create default admin account (username: admin, password: admin123)
    - _Requirements: 3.1, 8.2_

- [x] 12. Implement security features

  - [x] 12.1 Add CSRF protection

    - Configure Flask-WTF for CSRF tokens
    - Add CSRF tokens to all forms
    - _Requirements: 10.3_

  - [x] 12.2 Add input validation and sanitization

    - Validate all form inputs on server side
    - Sanitize user inputs to prevent injection attacks
    - _Requirements: 10.3_

  - [x] 12.3 Configure secure session management
    - Set secure session cookie flags
    - Configure session timeout
    - _Requirements: 1.4, 10.4_

- [ ] 13. Write unit tests

  - [x] 13.1 Write tests for User model

    - Test password hashing and verification
    - Test role checking methods
    - Test user creation and validation
    - _Requirements: 1.2, 1.3, 2.2, 2.3, 10.1, 10.2_

  - [x] 13.2 Write tests for Cluster model

    - Test total points calculation
    - Test logo URL generation
    - _Requirements: 6.2, 6.3_

  - [x] 13.3 Write tests for Event and Participant models

    - Test event creation with participants
    - Test participant grouping by cluster
    - Test validation constraints
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 13.4 Write tests for ActivityLog model
    - Test log entry creation
    - Test log detail formatting
    - _Requirements: 7.1, 7.2, 7.3, 7.6_

- [x] 14. Write integration tests

  - [x] 14.1 Write authentication flow tests

    - Test successful login with valid credentials
    - Test failed login with invalid credentials
    - Test session persistence
    - Test logout functionality
    - Test unauthorized access redirects
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 14.2 Write Event Manager CRUD tests

    - Test admin creating Event Manager account
    - Test admin updating Event Manager credentials
    - Test admin deleting Event Manager account
    - Test duplicate username prevention
    - Test non-admin access denial
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [x] 14.3 Write event management tests

    - Test creating event with multiple participants
    - Test editing existing event
    - Test deleting event
    - Test viewing event details
    - Test multiple participants from same cluster
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

  - [x] 14.4 Write overview calculation tests

    - Test correct point aggregation across events
    - Test proper cluster sorting by total points
    - Test real-time updates after event changes
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 14.5 Write activity logging tests
    - Test logs created for all Event Manager operations
    - Test log entries contain correct information
    - Test admin-only access to logs
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [x] 15. Create documentation and deployment files

  - [x] 15.1 Create README.md

    - Document installation instructions
    - Document usage instructions for Admin and Event Manager roles
    - Document how to replace cluster logos
    - Include troubleshooting section
    - _Requirements: 8.5_

  - [x] 15.2 Create .env.example file

    - List all required environment variables
    - Provide example values
    - _Requirements: 8.5_

  - [x] 15.3 Create database backup script
    - Write Python script to backup SQLite database
    - Include timestamp in backup filename
    - _Requirements: 8.3_

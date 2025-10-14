# Requirements Document

## Introduction

This document outlines the requirements for a Flask-based Event Scoring System that manages competitive events across 7 predefined clusters. The system provides role-based access control with Admin and Event Manager roles, allowing authorized users to create events, assign scores to participants from different clusters, and view aggregated cluster standings. The application runs entirely locally using SQLite for data persistence and includes comprehensive activity logging for accountability.

## Requirements

### Requirement 1: User Authentication and Authorization

**User Story:** As a system user, I want to log in with my username and password so that I can access features appropriate to my role.

#### Acceptance Criteria

1. WHEN a user navigates to the application THEN the system SHALL display a login page with username and password fields
2. WHEN a user submits valid credentials THEN the system SHALL authenticate the user and redirect them to the appropriate dashboard
3. WHEN a user submits invalid credentials THEN the system SHALL display an error message and remain on the login page
4. WHEN an authenticated user is idle THEN the system SHALL maintain the session until explicit logout
5. WHEN a user clicks logout THEN the system SHALL terminate the session and redirect to the login page
6. IF a user attempts to access protected routes without authentication THEN the system SHALL redirect them to the login page

### Requirement 2: Admin Account Management

**User Story:** As an Admin, I want to manage Event Manager accounts so that I can control who has access to create and manage events.

#### Acceptance Criteria

1. WHEN the Admin logs in THEN the system SHALL provide access to an Event Manager management interface
2. WHEN the Admin creates a new Event Manager account THEN the system SHALL require a unique username and password
3. WHEN the Admin creates a new Event Manager account THEN the system SHALL store the credentials securely in the database
4. WHEN the Admin views Event Manager accounts THEN the system SHALL display a list of all Event Manager usernames
5. WHEN the Admin deletes an Event Manager account THEN the system SHALL remove the account from the database
6. WHEN the Admin updates an Event Manager account THEN the system SHALL allow modification of username and password
7. IF the Admin attempts to create an Event Manager with a duplicate username THEN the system SHALL display an error message

### Requirement 3: Cluster Configuration

**User Story:** As a system administrator, I want the 7 clusters to be predefined in the system so that events can be organized consistently.

#### Acceptance Criteria

1. WHEN the system initializes THEN the system SHALL create 7 predefined clusters: Suryantra, Chandraloka, Swarnika, Ushnavi, Taraksha, Maya, and Meghora
2. WHEN displaying cluster information THEN the system SHALL support displaying cluster logos from uploaded image files
3. WHEN calculating cluster totals THEN the system SHALL use the predefined cluster names for aggregation
4. WHEN creating events THEN the system SHALL allow selection from the 7 predefined clusters only

### Requirement 4: Event Creation and Management

**User Story:** As an Event Manager or Admin, I want to create events with multiple participants and positions so that I can record competition results accurately.

#### Acceptance Criteria

1. WHEN an authorized user creates an event THEN the system SHALL require an event name
2. WHEN an authorized user adds participants to an event THEN the system SHALL allow specifying cluster affiliation, participant name, position, and points
3. WHEN an authorized user adds participants to an event THEN the system SHALL allow multiple participants from the same cluster
4. WHEN an authorized user adds participants to an event THEN the system SHALL allow multiple positions per event
5. WHEN an authorized user saves an event THEN the system SHALL persist all event data to the SQLite database
6. WHEN an authorized user views events THEN the system SHALL display a list of all created events
7. WHEN an authorized user edits an event THEN the system SHALL allow modification of event name, participants, positions, and points
8. WHEN an authorized user deletes an event THEN the system SHALL remove the event and all associated participant records

### Requirement 5: Event Display and Visualization

**User Story:** As an Event Manager or Admin, I want to view event results in a table format so that I can see competition outcomes clearly.

#### Acceptance Criteria

1. WHEN viewing an event THEN the system SHALL display the event name at the top
2. WHEN viewing an event THEN the system SHALL display a table with cluster logos in the left column
3. WHEN viewing an event THEN the system SHALL display participant names and points in the right column grouped by cluster
4. WHEN viewing an event with multiple participants from the same cluster THEN the system SHALL list all participants under that cluster's logo
5. WHEN viewing an event THEN the system SHALL display position information for each participant
6. WHEN viewing an event THEN the system SHALL use provided cluster logo images for visual identification

### Requirement 6: Cluster Overview and Leaderboard

**User Story:** As any authenticated user, I want to view total points per cluster so that I can see the overall standings across all events.

#### Acceptance Criteria

1. WHEN a user navigates to the overview tab THEN the system SHALL display a leaderboard of all 7 clusters
2. WHEN calculating cluster totals THEN the system SHALL sum all points earned by participants belonging to each cluster across all events
3. WHEN displaying the overview THEN the system SHALL show cluster names, logos, and total points
4. WHEN displaying the overview THEN the system SHALL sort clusters by total points in descending order
5. WHEN new events are added or modified THEN the system SHALL update cluster totals in real-time upon page refresh

### Requirement 7: Activity Logging and Audit Trail

**User Story:** As an Admin, I want to view logs of operations performed by Event Managers so that I can maintain accountability and track system usage.

#### Acceptance Criteria

1. WHEN an Event Manager creates an event THEN the system SHALL log the action with timestamp, username, and event details
2. WHEN an Event Manager edits an event THEN the system SHALL log the action with timestamp, username, and modified event details
3. WHEN an Event Manager deletes an event THEN the system SHALL log the action with timestamp, username, and deleted event name
4. WHEN an Admin views logs THEN the system SHALL display all logged operations in chronological order
5. WHEN an Admin views logs THEN the system SHALL display username, action type, timestamp, and relevant details for each log entry
6. WHEN the system logs operations THEN the system SHALL persist logs to the SQLite database

### Requirement 8: Local Deployment and Data Persistence

**User Story:** As a system administrator, I want the application to run entirely locally with SQLite so that no external services are required.

#### Acceptance Criteria

1. WHEN the application starts THEN the system SHALL use SQLite as the database engine
2. WHEN the application starts THEN the system SHALL create necessary database tables if they don't exist
3. WHEN the application runs THEN the system SHALL store all data (users, events, participants, logs) in a local SQLite file
4. WHEN the application serves static files THEN the system SHALL serve HTML, CSS, JavaScript, and images from local directories
5. WHEN the application is deployed THEN the system SHALL require only Python and Flask dependencies without external database servers

### Requirement 9: User Interface and Navigation

**User Story:** As any authenticated user, I want an intuitive interface with clear navigation so that I can efficiently perform my tasks.

#### Acceptance Criteria

1. WHEN a user is authenticated THEN the system SHALL display a navigation menu with available options based on user role
2. WHEN an Admin is authenticated THEN the system SHALL display navigation options for: Overview, Events, Event Manager Management, and Logs
3. WHEN an Event Manager is authenticated THEN the system SHALL display navigation options for: Overview and Events
4. WHEN a user navigates between pages THEN the system SHALL maintain consistent layout and styling
5. WHEN a user performs actions THEN the system SHALL provide visual feedback (success/error messages)
6. WHEN displaying forms THEN the system SHALL include appropriate input validation and error messages

### Requirement 10: Security and Data Integrity

**User Story:** As a system administrator, I want user passwords to be stored securely so that account credentials are protected.

#### Acceptance Criteria

1. WHEN a user account is created THEN the system SHALL hash passwords before storing them in the database
2. WHEN a user logs in THEN the system SHALL compare hashed passwords for authentication
3. WHEN the system stores sensitive data THEN the system SHALL use appropriate security measures to prevent SQL injection
4. WHEN users access the application THEN the system SHALL use session management to maintain authentication state securely
5. IF an unauthorized user attempts to access admin-only features THEN the system SHALL deny access and redirect appropriately

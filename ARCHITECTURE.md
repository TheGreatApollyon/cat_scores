# Event Scoring System - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         PUBLIC ACCESS                            │
│                      (No Authentication)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GET /              → Redirect to /overview                     │
│  GET /overview      → Public Leaderboard                        │
│                       - View cluster standings                   │
│                       - Real-time point totals                   │
│                       - Cluster logos                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                              ↓ Click "Login to Manage"

┌─────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GET/POST /login    → Login Page                                │
│                       - Username & Password                      │
│                       - Session Creation                         │
│                       - Role Assignment                          │
│                                                                  │
│  GET /logout        → Clear Session                             │
│                       - Redirect to Public View                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                              ↓ After Login

┌─────────────────────────────────────────────────────────────────┐
│                    MANAGEMENT ACCESS                             │
│              (Authentication Required)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GET /manage        → Management Dashboard                       │
│                       - Quick access to all features             │
│                       - Role-based menu                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              EVENT MANAGEMENT                               │ │
│  │  (Event Managers & Admins)                                 │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  GET  /manage/events/           → List all events          │ │
│  │  GET  /manage/events/create     → Create event form        │ │
│  │  POST /manage/events/create     → Save new event           │ │
│  │  GET  /manage/events/<id>       → View event details       │ │
│  │  GET  /manage/events/<id>/edit  → Edit event form          │ │
│  │  POST /manage/events/<id>/edit  → Update event             │ │
│  │  POST /manage/events/<id>/delete → Delete event            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           ADMIN-ONLY FEATURES                              │ │
│  │  (Administrators Only)                                     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  GET  /manage/admin/managers          → List managers     │ │
│  │  POST /manage/admin/managers/create   → Create manager    │ │
│  │  POST /manage/admin/managers/<id>/edit → Edit manager     │ │
│  │  POST /manage/admin/managers/<id>/delete → Delete manager │ │
│  │                                                            │ │
│  │  GET  /manage/admin/logs              → View activity logs│ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       ↓
┌──────────────────────────────────────────┐
│         Flask Application                 │
│  ┌────────────────────────────────────┐  │
│  │      Route Handlers                │  │
│  │  - auth.py    (Login/Logout)       │  │
│  │  - overview.py (Public/Dashboard)  │  │
│  │  - events.py  (Event CRUD)         │  │
│  │  - admin.py   (Manager CRUD)       │  │
│  │  - logs.py    (Activity Logs)      │  │
│  └────────────────────────────────────┘  │
│                    ↓                      │
│  ┌────────────────────────────────────┐  │
│  │      Decorators & Utils            │  │
│  │  - @login_required                 │  │
│  │  - @admin_required                 │  │
│  │  - log_activity()                  │  │
│  └────────────────────────────────────┘  │
│                    ↓                      │
│  ┌────────────────────────────────────┐  │
│  │      SQLAlchemy Models             │  │
│  │  - User                            │  │
│  │  - Cluster                         │  │
│  │  - Event                           │  │
│  │  - Participant                     │  │
│  │  - ActivityLog                     │  │
│  └────────────────────────────────────┘  │
└──────────────────┬───────────────────────┘
                   │
                   ↓
         ┌─────────────────┐
         │  SQLite Database │
         │  event_scoring.db│
         └─────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Route Protection                                  │
│  ├─ Public routes: No authentication                        │
│  ├─ Protected routes: @login_required                       │
│  └─ Admin routes: @admin_required                           │
│                                                              │
│  Layer 2: Session Management                                │
│  ├─ Flask sessions with secure cookies                      │
│  ├─ User ID, username, role stored                          │
│  └─ 24-hour session lifetime                                │
│                                                              │
│  Layer 3: Password Security                                 │
│  ├─ PBKDF2-SHA256 hashing                                   │
│  ├─ Werkzeug security utilities                             │
│  └─ No plaintext passwords                                  │
│                                                              │
│  Layer 4: CSRF Protection                                   │
│  ├─ Flask-WTF CSRF tokens                                   │
│  ├─ All forms protected                                     │
│  └─ Token validation on POST                                │
│                                                              │
│  Layer 5: Input Validation                                  │
│  ├─ Server-side validation                                  │
│  ├─ SQLAlchemy ORM (SQL injection prevention)              │
│  └─ Type checking and constraints                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## User Roles & Permissions

```
┌─────────────────────────────────────────────────────────────┐
│                      PUBLIC USER                             │
├─────────────────────────────────────────────────────────────┤
│  ✅ View leaderboard                                         │
│  ✅ See cluster standings                                    │
│  ✅ View total points                                        │
│  ❌ Cannot modify anything                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   EVENT MANAGER                              │
├─────────────────────────────────────────────────────────────┤
│  ✅ View leaderboard                                         │
│  ✅ Access management dashboard                              │
│  ✅ Create events                                            │
│  ✅ Edit events                                              │
│  ✅ Delete events                                            │
│  ✅ Add/remove participants                                  │
│  ❌ Cannot manage other users                                │
│  ❌ Cannot view activity logs                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    ADMINISTRATOR                             │
├─────────────────────────────────────────────────────────────┤
│  ✅ All Event Manager permissions                            │
│  ✅ Create Event Manager accounts                            │
│  ✅ Edit Event Manager accounts                              │
│  ✅ Delete Event Manager accounts                            │
│  ✅ View activity logs                                       │
│  ✅ Full system access                                       │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ password_hash   │
│ role            │
│ created_at      │
└────────┬────────┘
         │
         │ created_by
         ↓
┌─────────────────┐         ┌─────────────────┐
│     events      │         │    clusters     │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ name            │         │ name            │
│ created_by (FK) │         │ logo_filename   │
│ created_at      │         │ created_at      │
│ updated_at      │         └────────┬────────┘
└────────┬────────┘                  │
         │                           │
         │ event_id         cluster_id
         ↓                           ↓
         ┌─────────────────────────────┐
         │      participants           │
         ├─────────────────────────────┤
         │ id (PK)                     │
         │ event_id (FK)               │
         │ cluster_id (FK)             │
         │ name                        │
         │ position                    │
         │ points                      │
         │ created_at                  │
         └─────────────────────────────┘

┌─────────────────┐
│  activity_logs  │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ action          │
│ details (JSON)  │
│ timestamp       │
└─────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND                                  │
├─────────────────────────────────────────────────────────────┤
│  HTML5          - Semantic markup                            │
│  CSS3           - Responsive design, Flexbox/Grid            │
│  JavaScript     - Dynamic forms, Client validation           │
│  Jinja2         - Server-side templating                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BACKEND                                   │
├─────────────────────────────────────────────────────────────┤
│  Flask 3.0      - Web framework                              │
│  Flask-Login    - Session management                         │
│  Flask-WTF      - CSRF protection                            │
│  SQLAlchemy     - ORM                                        │
│  Werkzeug       - Password hashing                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DATABASE                                  │
├─────────────────────────────────────────────────────────────┤
│  SQLite 3       - Local database                             │
│  Auto-migration - Schema creation on startup                 │
│  Backup script  - Manual backup utility                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    TESTING                                   │
├─────────────────────────────────────────────────────────────┤
│  pytest         - Test framework                             │
│  Playwright     - E2E testing                                │
│  Flask test     - Integration testing                        │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT                                │
├─────────────────────────────────────────────────────────────┤
│  Flask dev server (127.0.0.1:5000)                          │
│  SQLite database                                             │
│  Debug mode enabled                                          │
│  Auto-reload on changes                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   PRODUCTION                                 │
├─────────────────────────────────────────────────────────────┤
│  WSGI server (Gunicorn/uWSGI)                               │
│  Nginx reverse proxy                                         │
│  HTTPS enabled                                               │
│  Secure cookies                                              │
│  Database backups                                            │
│  Log rotation                                                │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

1. **Public-First Approach**

   - Root URL shows public leaderboard
   - No barriers to viewing standings
   - Management clearly separated

2. **Role-Based Access Control**

   - Decorator-based protection
   - Clear permission boundaries
   - Admin vs Event Manager roles

3. **SQLite for Simplicity**

   - No external database required
   - Easy backup and restore
   - Perfect for local deployment

4. **Session-Based Auth**

   - Simple and secure
   - No JWT complexity
   - Server-side session storage

5. **Activity Logging**

   - Audit trail for accountability
   - JSON details for flexibility
   - Admin-only access

6. **Responsive Design**
   - Mobile-friendly
   - Flexbox/Grid layout
   - Works on all devices

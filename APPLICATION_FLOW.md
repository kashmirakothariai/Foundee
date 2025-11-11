# Foundee - Application Flow Diagrams

**Owner:** Gaurang Kothari (X Googler)

## System Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │◄────────┤   FastAPI       │◄────────┤   PostgreSQL    │
│  (Port 3000)    │  HTTP   │   Backend       │  SQL    │   Database      │
│                 │  REST   │  (Port 8000)    │         │                 │
└────────┬────────┘         └────────┬────────┘         └─────────────────┘
         │                           │
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│  Google OAuth   │         │   SMTP Server   │
│  Authentication │         │  (Gmail/Other)  │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
```

## User Registration Flow

```
┌────────┐
│ User   │
└───┬────┘
    │
    ├─► Visit http://localhost:3000
    │
    ├─► Click "Sign in with Google"
    │
    ├─► Google OAuth Popup Opens
    │   ├─► User selects Google account
    │   └─► Google sends token
    │
    ├─► Frontend sends token to Backend
    │   POST /api/auth/google-login
    │
    ├─► Backend verifies token with Google
    │
    ├─► Backend checks if user exists
    │   │
    │   ├─► If NEW:
    │   │   ├─► Create user_login record
    │   │   └─► Create empty user_dtls record
    │   │
    │   └─► If EXISTS:
    │       └─► Retrieve existing user
    │
    ├─► Backend creates JWT token
    │
    ├─► Frontend stores token in localStorage
    │
    └─► Redirect to Dashboard
```

## QR Code Creation Flow

```
┌────────┐
│ Owner  │
└───┬────┘
    │
    ├─► Login (if not logged in)
    │
    ├─► Go to Dashboard
    │
    ├─► Click "Create New QR"
    │
    ├─► Frontend: POST /api/qr/create
    │   Headers: { Authorization: "Bearer <token>" }
    │
    ├─► Backend validates JWT token
    │
    ├─► Backend creates qr_dtls record
    │   ├─► Generate UUID for QR
    │   ├─► Set user_id to current user
    │   ├─► Set all permissions to TRUE
    │   └─► Save to database
    │
    ├─► Return QR details to Frontend
    │
    ├─► Frontend generates QR image
    │   URL: http://localhost:3000/qr/{uuid}
    │
    ├─► Display QR on Dashboard
    │
    └─► User can download QR image
```

## QR Code Scanning Flow (Finder)

```
┌────────┐
│ Finder │
└───┬────┘
    │
    ├─► Open http://localhost:3000/scan
    │   (No login required)
    │
    ├─► Click "Start Scanning"
    │
    ├─► Browser requests camera permission
    │
    ├─► User grants permission
    │
    ├─► Scan QR code with camera
    │
    ├─► QR decoded: http://localhost:3000/qr/{uuid}
    │
    ├─► Browser requests location permission
    │
    ├─► User grants permission (optional)
    │
    ├─► Frontend: GET /api/qr/scan/{uuid}?lat=X&lng=Y
    │   (No auth token needed)
    │
    ├─► Backend processes scan
    │   │
    │   ├─► Create qr_usage record (log scan)
    │   │   ├─► qr_id: {uuid}
    │   │   ├─► latitude: X
    │   │   └─► longitude: Y
    │   │
    │   ├─► Get QR owner's user_id
    │   │
    │   ├─► Get user_dtls for owner
    │   │
    │   ├─► Get qr_dtls permissions
    │   │
    │   ├─► Filter user details by permissions
    │   │   ├─► If first_name = TRUE → include
    │   │   ├─► If mobile_no = FALSE → exclude
    │   │   └─► etc.
    │   │
    │   └─► Send email to owner
    │       ├─► To: owner.email_id
    │       ├─► Subject: "QR Code Scanned"
    │       ├─► Body: Location + Time
    │       └─► Via SMTP
    │
    ├─► Display filtered contact info
    │   ├─► Name (if visible)
    │   ├─► Phone (if visible)
    │   ├─► Email (if visible)
    │   └─► etc.
    │
    └─► Finder contacts owner to return item
```

## Owner Scans Own QR Flow

```
┌────────┐
│ Owner  │
└───┬────┘
    │
    ├─► Scan own QR code
    │
    ├─► Frontend: GET /api/qr/scan/{uuid}
    │   Headers: { Authorization: "Bearer <token>" }
    │
    ├─► Backend checks if scanner is owner
    │   qr.user_id == current_user.id
    │
    ├─► Backend returns is_owner = TRUE
    │
    ├─► Frontend redirects to Update Panel
    │   Navigate to: /update/{uuid}
    │
    └─► Owner can edit details
```

## Update Panel Flow

```
┌────────┐
│ Owner  │
└───┬────┘
    │
    ├─► Navigate to /update/{uuid}
    │
    ├─► Check if logged in
    │   └─► If NO: Redirect to /login
    │
    ├─► Frontend: GET /api/user/details
    │   GET /api/qr/details/{uuid}
    │   Headers: { Authorization: "Bearer <token>" }
    │
    ├─► Backend validates ownership
    │   qr.user_id == current_user.id
    │
    ├─► Load current details and permissions
    │
    ├─► Display Update Panel
    │   ├─► Text fields for each detail
    │   └─► Checkbox for each permission
    │
    ├─► User edits information
    │   ├─► Change "First Name" to "John"
    │   ├─► Change "Mobile" to "123-456-7890"
    │   └─► Uncheck "Address" visibility
    │
    ├─► Click "Save Changes"
    │
    ├─► Frontend: PUT /api/user/details
    │   PUT /api/qr/update-permissions/{uuid}
    │   Headers: { Authorization: "Bearer <token>" }
    │
    ├─► Backend updates database
    │   ├─► Update user_dtls table
    │   │   ├─► first_name = "John"
    │   │   └─► mobile_no = "123-456-7890"
    │   │
    │   └─► Update qr_dtls table
    │       └─► address = FALSE
    │
    ├─► Return success response
    │
    └─► Display "Details updated successfully!"
```

## Email Notification Flow

```
┌─────────┐
│ Backend │
└────┬────┘
     │
     ├─► QR scanned event triggered
     │
     ├─► Get owner's email from user_login
     │
     ├─► Compose email
     │   ├─► To: owner.email_id
     │   ├─► From: SMTP_USER
     │   ├─► Subject: "Foundee Alert: QR Scanned"
     │   └─► Body:
     │       ├─► QR ID: {uuid}
     │       ├─► Location: {lat}, {lng}
     │       ├─► Google Maps link
     │       └─► Timestamp
     │
     ├─► Connect to SMTP server
     │   ├─► Host: smtp.gmail.com
     │   ├─► Port: 587
     │   ├─► TLS: Yes
     │   └─► Auth: SMTP_USER + SMTP_PASSWORD
     │
     ├─► Send email via SMTP
     │
     └─► Owner receives email notification
```

## Database Schema Flow

```
user_login (Authentication)
    ├─── id (UUID, PK)
    ├─── name
    ├─── email_id (unique)
    ├─── password (optional)
    ├─── active_flag
    └─── timestamps
         │
         ├─► 1:1 relationship
         │
         ▼
user_dtls (Personal Info)
    ├─── id (UUID, PK)
    ├─── user_id (FK)
    ├─── first_name
    ├─── last_name
    ├─── mobile_no
    ├─── address
    ├─── email_id
    ├─── blood_grp
    ├─── company_name
    ├─── description
    └─── timestamps

user_login
    │
    ├─► 1:Many relationship
    │
    ▼
qr_dtls (QR Codes & Permissions)
    ├─── id (UUID, PK)
    ├─── user_id (FK)
    ├─── first_name (bool)
    ├─── last_name (bool)
    ├─── mobile_no (bool)
    ├─── address (bool)
    ├─── email_id (bool)
    ├─── blood_grp (bool)
    ├─── company_name (bool)
    ├─── description (bool)
    └─── timestamps
         │
         ├─► 1:Many relationship
         │
         ▼
qr_usage (Scan History)
    ├─── id (UUID, PK)
    ├─── qr_id (FK)
    ├─── latitude
    ├─── longitude
    └─── timestamps
```

## Authentication Flow

```
Every Request with Auth:
    │
    ├─► Frontend includes header:
    │   Authorization: Bearer <JWT_TOKEN>
    │
    ├─► Backend middleware intercepts
    │
    ├─► Extract token from header
    │
    ├─► Verify JWT signature with SECRET_KEY
    │
    ├─► Check token expiration
    │   └─► If expired: Return 401 Unauthorized
    │
    ├─► Extract user_id from token payload
    │
    ├─► Query database for user
    │   SELECT * FROM user_login WHERE email_id = ?
    │
    ├─► If user not found: Return 401
    │
    ├─► Attach user to request context
    │
    └─► Continue to endpoint handler
```

## Privacy Control Flow

```
Scanner requests QR info:
    │
    ├─► Backend receives: GET /api/qr/scan/{uuid}
    │
    ├─► Query qr_dtls for permissions
    │   first_name = TRUE
    │   mobile_no = TRUE
    │   address = FALSE
    │   email_id = TRUE
    │   ...
    │
    ├─► Query user_dtls for actual data
    │   first_name = "John"
    │   mobile_no = "555-1234"
    │   address = "123 Main St"
    │   email_id = "john@email.com"
    │   ...
    │
    ├─► Apply permission filter
    │   ├─► first_name (TRUE) → Include "John"
    │   ├─► mobile_no (TRUE) → Include "555-1234"
    │   ├─► address (FALSE) → EXCLUDE
    │   └─► email_id (TRUE) → Include "john@email.com"
    │
    └─► Return filtered response
        {
          "first_name": "John",
          "mobile_no": "555-1234",
          "email_id": "john@email.com"
          // address NOT included
        }
```

---

**Built by Gaurang Kothari (X Googler)**


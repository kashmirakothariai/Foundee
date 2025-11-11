# Foundee - Project Structure

```
Foundee/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI application entry point
│   │   ├── config.py                # Configuration management
│   │   ├── database.py              # Database connection and session
│   │   ├── models.py                # SQLAlchemy database models
│   │   ├── schemas.py               # Pydantic schemas for validation
│   │   ├── auth.py                  # Authentication & JWT handling
│   │   ├── encryption.py            # Optional encryption service
│   │   ├── email_service.py         # Email notification service
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py              # Authentication endpoints
│   │       ├── user.py              # User management endpoints
│   │       └── qr.py                # QR code endpoints
│   │
│   ├── alembic/                     # Database migrations
│   │   ├── versions/                # Migration files
│   │   ├── env.py                   # Alembic environment config
│   │   └── script.py.mako           # Migration template
│   │
│   ├── alembic.ini                  # Alembic configuration
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   ├── .env                         # Environment variables (ignored)
│   └── .gitignore                   # Git ignore rules
│
├── frontend/                         # React Frontend
│   ├── public/
│   │   └── index.html               # HTML template
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js             # Login page with Google OAuth
│   │   │   ├── Login.css
│   │   │   ├── Dashboard.js         # User dashboard
│   │   │   ├── Dashboard.css
│   │   │   ├── QRScanner.js         # QR code scanner
│   │   │   ├── QRScanner.css
│   │   │   ├── QRView.js            # QR code information view
│   │   │   ├── QRView.css
│   │   │   ├── UpdatePanel.js       # Edit details & permissions
│   │   │   └── UpdatePanel.css
│   │   │
│   │   ├── utils/
│   │   │   └── api.js               # API client and endpoints
│   │   │
│   │   ├── App.js                   # Main app component
│   │   ├── App.css                  # Global app styles
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Global styles
│   │
│   ├── package.json                 # Node dependencies
│   ├── .env.example                 # Environment variables template
│   ├── .env                         # Environment variables (ignored)
│   └── .gitignore                   # Git ignore rules
│
├── README.md                         # Main documentation
├── SETUP_INSTRUCTIONS.md            # Setup guide
├── PROJECT_STRUCTURE.md             # This file
├── setup.sh                         # Linux/Mac setup script
└── setup.bat                        # Windows setup script
```

## Database Schema

### user_login
- Primary user authentication table
- Fields: id, name, email_id, password, active_flag, timestamps

### user_dtls
- Detailed user information
- Fields: id, user_id (FK), first_name, last_name, mobile_no, address, email_id, blood_grp, company_name, description, timestamps

### qr_dtls
- QR codes and visibility permissions
- Fields: id, user_id (FK), first_name (bool), last_name (bool), mobile_no (bool), address (bool), email_id (bool), blood_grp (bool), company_name (bool), description (bool), timestamps

### qr_usage
- QR scan history with location
- Fields: id, qr_id (FK), latitude, longitude, timestamps

## Key Features by Component

### Backend (FastAPI)
- ✅ Google OAuth 2.0 authentication
- ✅ JWT token-based sessions
- ✅ RESTful API with automatic docs
- ✅ PostgreSQL with SQLAlchemy ORM
- ✅ Alembic database migrations
- ✅ Email notifications via SMTP
- ✅ Optional encryption service
- ✅ CORS middleware
- ✅ Error handling

### Frontend (React)
- ✅ Google OAuth login button
- ✅ QR code generation (with qrcode library)
- ✅ QR code scanning (with html5-qrcode)
- ✅ User dashboard
- ✅ Detail update panel with permissions
- ✅ Geolocation capture
- ✅ Responsive design
- ✅ Modern gradient UI

## API Endpoints

### Authentication
- `POST /api/auth/google-login` - Google OAuth login
- `POST /api/auth/login` - Email/password login

### Users
- `GET /api/user/me` - Get current user
- `GET /api/user/details` - Get user details
- `PUT /api/user/details` - Update user details

### QR Codes
- `POST /api/qr/create` - Create QR code (auth required)
- `GET /api/qr/scan/{qr_id}` - Scan QR (public)
- `GET /api/qr/details/{qr_id}` - Get QR details (owner only)
- `PUT /api/qr/update-permissions/{qr_id}` - Update permissions
- `PUT /api/qr/bind/{qr_id}` - Bind QR to user
- `GET /api/qr/my-qr-codes` - Get user's QR codes

## User Flows

### New User Registration
1. User scans QR or visits site
2. Clicks "Sign in with Google"
3. Authenticates via Google OAuth
4. Account created automatically
5. Empty user_details record created

### QR Code Creation
1. User logs in
2. Goes to Dashboard
3. Clicks "Create New QR"
4. QR code generated with UUID
5. User can download QR image

### Scanning Someone's QR
1. Finder scans QR (no login needed)
2. Location captured automatically
3. Filtered contact info displayed
4. Email sent to owner with location
5. Finder can contact owner

### Owner Updates Details
1. Owner scans their own QR
2. Redirected to Update Panel
3. Can edit all personal fields
4. Toggle visibility for each field
5. Changes saved to user_dtls and qr_dtls

## Security Considerations

- JWT tokens expire after 30 minutes (configurable)
- Passwords hashed with bcrypt
- Optional field-level encryption
- SQL injection prevention via ORM
- CORS restricted to specific origins
- Google OAuth for secure authentication
- No sensitive data in URLs

## Environment Variables

### Backend
- DATABASE_URL - PostgreSQL connection
- SECRET_KEY - JWT signing key
- GOOGLE_CLIENT_ID - OAuth client ID
- GOOGLE_CLIENT_SECRET - OAuth secret
- SMTP_* - Email configuration
- ENCRYPTION_ENABLED - Encryption flag

### Frontend
- REACT_APP_API_URL - Backend URL
- REACT_APP_GOOGLE_CLIENT_ID - OAuth client ID

## Technologies Used

### Backend
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Alembic 1.12.1
- psycopg2-binary 2.9.9
- python-jose (JWT)
- passlib (password hashing)
- google-auth (OAuth)

### Frontend
- React 18.2.0
- React Router 6.20.0
- Axios 1.6.2
- html5-qrcode 2.3.8
- qrcode 1.5.3
- @react-oauth/google 0.12.1

---

**Owner: Gaurang Kothari (X Googler)**


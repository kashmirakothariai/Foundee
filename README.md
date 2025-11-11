# Foundee - QR-Based Lost and Found Application

**Owner:** Gaurang Kothari (X Googler)

Foundee is a QR code-based lost and found application that helps people recover their lost items by providing contact information to those who find them.

## Features

- 🔐 **Google OAuth Authentication** - Secure login with Gmail
- 📱 **QR Code Generation** - Create unique QR codes for your belongings
- 🎯 **QR Scanning** - Scan QR codes to view owner information
- 🔒 **Granular Privacy Controls** - Control which information is visible
- 📍 **Location Tracking** - Automatic location capture when QR is scanned
- 📧 **Email Notifications** - Get notified when your QR code is scanned
- 👤 **User Roles** - ASP Admin (full access) and regular Users
- 🔐 **End-to-End Encryption** - Optional encryption for sensitive data

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **Alembic** - Database migrations
- **SQLAlchemy** - ORM
- **Google OAuth 2.0** - Authentication
- **JWT** - Token-based authentication

### Frontend
- **React 18** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **html5-qrcode** - QR code scanning
- **qrcode** - QR code generation
- **Google OAuth** - Authentication

## Database Schema

### Tables

1. **user_login** - User authentication and profile
2. **user_dtls** - Detailed user information
3. **qr_dtls** - QR codes and visibility permissions
4. **qr_usage** - QR scan history with location

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Gmail account for OAuth

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/foundee_db
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

6. Create database:
```bash
createdb foundee_db
```

7. Run migrations:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

8. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000
API documentation: http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

5. Start the development server:
```bash
npm start
```

The app will be available at http://localhost:3000

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized JavaScript origins: `http://localhost:3000`
   - Authorized redirect URIs: `http://localhost:3000`
5. Copy Client ID and Client Secret to your `.env` files

## Gmail SMTP Setup (for email notifications)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings → Security
   - Select "App passwords"
   - Generate new app password for "Mail"
3. Use this app password in `SMTP_PASSWORD` environment variable

## Usage

### For QR Code Owners

1. **Sign in** with your Google account
2. **Create QR codes** from your dashboard
3. **Download** and print QR codes
4. **Attach** QR codes to your belongings
5. **Update details** and privacy settings anytime
6. **Receive email** notifications when someone scans your QR

### For Finders

1. **Scan QR code** (no login required)
2. **View contact information** (based on owner's privacy settings)
3. **Contact the owner** to return the item
4. Owner receives automatic email with your scan location

### For ASP Admin

1. Sign in with admin account
2. Access all user data
3. View and edit any user details
4. Monitor QR usage across platform

## API Endpoints

### Authentication
- `POST /api/auth/google-login` - Login with Google OAuth
- `POST /api/auth/login` - Login with email/password

### User Management
- `GET /api/user/me` - Get current user info
- `GET /api/user/details` - Get user details
- `PUT /api/user/details` - Update user details

### QR Code Management
- `POST /api/qr/create` - Create new QR code
- `GET /api/qr/scan/{qr_id}` - Scan QR code (public)
- `GET /api/qr/details/{qr_id}` - Get QR details (owner only)
- `PUT /api/qr/update-permissions/{qr_id}` - Update visibility permissions
- `PUT /api/qr/bind/{qr_id}` - Bind QR to user
- `GET /api/qr/my-qr-codes` - Get user's QR codes

## Security Features

- **JWT Authentication** - Secure token-based auth
- **Google OAuth** - No password storage needed
- **Granular Permissions** - Field-level privacy control
- **Optional Encryption** - End-to-end encryption flag
- **CORS Protection** - Configured origins
- **SQL Injection Protection** - ORM-based queries

## Development

### Running Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Database Management

The application uses Alembic for database migrations. All tables include:
- UUID primary keys
- Active flags for soft deletes
- Creation and update timestamps
- User tracking (created by, updated by)

## Production Deployment

### Backend

1. Set `ENCRYPTION_ENABLED=true` in production
2. Generate secure `SECRET_KEY` and `ENCRYPTION_KEY`
3. Use production PostgreSQL database
4. Configure HTTPS
5. Set up proper CORS origins
6. Use production SMTP server

### Frontend

1. Build production bundle:
```bash
npm run build
```

2. Serve with nginx or similar
3. Update `REACT_APP_API_URL` to production API
4. Configure production Google OAuth credentials

## License

Proprietary - All rights reserved by Gaurang Kothari

## Support

For issues or questions, please contact the development team.

---

**Built with ❤️ by Gaurang Kothari (X Googler)**


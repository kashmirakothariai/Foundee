# Foundee - Quick Setup Instructions

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **PostgreSQL 13+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

## Quick Setup (Automated)

### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
```

### Windows
```bash
setup.bat
```

## Manual Setup

### Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

### Step 2: Configure Backend Environment

Edit `backend/.env`:

```env
# Database (change credentials)
DATABASE_URL=postgresql://postgres:password@localhost:5432/foundee_db

# Security (generate secure keys)
SECRET_KEY=your-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth (get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Encryption (optional, for production)
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=generate-with-fernet-generate-key

# CORS
FRONTEND_URL=http://localhost:3000

# Email (use Gmail App Password)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-digit-app-password
```

### Step 3: Setup Database

```bash
# Create database
createdb foundee_db

# Or using psql
psql -U postgres
CREATE DATABASE foundee_db;
\q

# Run migrations
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Step 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your Google Client ID
```

### Step 5: Configure Frontend Environment

Edit `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

### Step 6: Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Application type: **Web application**
6. Add authorized origins:
   - `http://localhost:3000`
   - `http://localhost:8000`
7. Add authorized redirect URIs:
   - `http://localhost:3000`
8. Copy **Client ID** and **Client Secret**
9. Update both `.env` files

### Step 7: Gmail SMTP Setup (for notifications)

1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account → Security → App passwords
3. Generate app password for "Mail"
4. Use this 16-digit password in `SMTP_PASSWORD`

### Step 8: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Testing the Application

1. Open http://localhost:3000
2. Click "Continue without login" to scan QR (or login with Google)
3. After login, create a QR code from dashboard
4. Download and test scanning the QR code

## Common Issues

### Port Already in Use
- Backend: Change port in uvicorn command: `--port 8001`
- Frontend: Change port via environment variable: `PORT=3001 npm start`

### Database Connection Error
- Verify PostgreSQL is running: `sudo service postgresql status`
- Check DATABASE_URL credentials in backend/.env
- Ensure database exists: `psql -l`

### Google OAuth Error
- Verify Client ID is correct in both .env files
- Check authorized origins in Google Console
- Clear browser cache and try again

### SMTP Email Error
- Verify Gmail App Password (not regular password)
- Check 2FA is enabled on Gmail
- Ensure "Less secure app access" is NOT needed (use App Password)

## Project Structure

```
Foundee/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── auth.py          # Authentication
│   │   ├── database.py      # DB connection
│   │   └── main.py          # FastAPI app
│   ├── alembic/             # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── utils/           # API utilities
│   │   └── App.js           # Main app
│   ├── package.json         # Node dependencies
│   └── .env                 # Environment variables
└── README.md                # Documentation
```

## Next Steps

- Customize UI styling
- Add more QR code sizes
- Implement admin panel
- Deploy to production
- Add more notification channels

## Support

For issues or questions, refer to README.md or contact the development team.

---

**Built by Gaurang Kothari (X Googler)**


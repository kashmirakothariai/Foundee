# Foundee - Quick Start Guide

**Owner:** Gaurang Kothari (X Googler)

Get Foundee up and running in under 10 minutes!

## Prerequisites Check

Make sure you have:
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] PostgreSQL 13+ installed (`psql --version`)
- [ ] Google account for OAuth setup

## 5-Minute Setup

### 1. Clone and Setup (2 minutes)

**Windows:**
```bash
# Navigate to project
cd E:\Hardik\Product\Foundee

# Run setup
setup.bat
```

**Linux/Mac:**
```bash
# Navigate to project
cd /path/to/Foundee

# Make executable and run
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment (3 minutes)

**Backend Configuration:**

Edit `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/foundee_db
SECRET_KEY=change-this-to-a-random-32-character-string
GOOGLE_CLIENT_ID=get-from-google-console
GOOGLE_CLIENT_SECRET=get-from-google-console
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-digit-app-password
```

**Frontend Configuration:**

Edit `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=same-as-backend-client-id
```

### 3. Get Google OAuth Credentials (3 minutes)

1. Visit: https://console.cloud.google.com/
2. Create new project: "Foundee"
3. Enable API: "Google+ API"
4. Create Credentials → OAuth 2.0 Client ID
5. Application type: Web application
6. Authorized origins: `http://localhost:3000`, `http://localhost:8000`
7. Copy Client ID and Secret to .env files

### 4. Setup Database (1 minute)

```bash
# Create database
createdb -U postgres foundee_db

# Or via psql
psql -U postgres
CREATE DATABASE foundee_db;
\q

# Run migrations
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Start Application (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Test It Out!

1. Open http://localhost:3000
2. Click "Sign in with Google"
3. Authenticate
4. Create your first QR code
5. Download and scan it!

## Quick Commands Reference

### Backend
```bash
# Activate environment
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run server
uvicorn app.main:app --reload

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend
```bash
# Start dev server
cd frontend
npm start

# Build for production
npm run build

# Install new package
npm install package-name
```

### Database
```bash
# Connect to database
psql -U postgres -d foundee_db

# List tables
\dt

# Describe table
\d table_name

# Exit
\q
```

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is free
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend won't start
```bash
# Check if port 3000 is free
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### Database connection error
```bash
# Check PostgreSQL is running
# Windows: Services → PostgreSQL
# Linux: sudo service postgresql status
# Mac: brew services list

# Test connection
psql -U postgres -d foundee_db -c "SELECT 1"
```

### Google OAuth not working
- Clear browser cookies
- Check Client ID matches in both .env files
- Verify authorized origins in Google Console
- Try incognito mode

### Email notifications not sending
- Use Gmail App Password (not regular password)
- Enable 2-Factor Authentication first
- Check SMTP credentials in backend/.env
- Test with: https://www.smtper.net/

## Project URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Interactive API:** http://localhost:8000/redoc

## Key Files to Know

- `backend/app/main.py` - API entry point
- `backend/app/routes/qr.py` - QR endpoints
- `frontend/src/App.js` - React app
- `frontend/src/components/Dashboard.js` - Main dashboard
- `backend/.env` - Backend config
- `frontend/.env` - Frontend config

## Common Tasks

### Add a new API endpoint
1. Edit `backend/app/routes/[module].py`
2. Add route function with decorator
3. Test at http://localhost:8000/docs

### Add a new React page
1. Create component in `frontend/src/components/`
2. Add route in `frontend/src/App.js`
3. Add navigation link

### Modify database schema
1. Edit `backend/app/models.py`
2. Create migration: `alembic revision --autogenerate -m "Description"`
3. Apply: `alembic upgrade head`

### Change styling
1. Edit component CSS file in `frontend/src/components/`
2. Or edit global styles in `frontend/src/App.css`

## Default Accounts

There are no default accounts. All users register via Google OAuth.

To create an admin user, manually update the database:
```sql
-- Connect to database
psql -U postgres -d foundee_db

-- Update user to admin (implement admin logic in backend)
UPDATE user_login SET is_admin = true WHERE email_id = 'admin@example.com';
```

## Production Deployment Checklist

Backend:
- [ ] Set `ENCRYPTION_ENABLED=true`
- [ ] Generate secure SECRET_KEY (32+ characters)
- [ ] Use production PostgreSQL
- [ ] Configure HTTPS
- [ ] Set proper CORS origins
- [ ] Use production SMTP
- [ ] Set up logging

Frontend:
- [ ] Update REACT_APP_API_URL to production
- [ ] Update Google OAuth credentials
- [ ] Build: `npm run build`
- [ ] Serve with nginx/Apache
- [ ] Enable HTTPS

## Need Help?

1. Check `README.md` for detailed documentation
2. Check `SETUP_INSTRUCTIONS.md` for step-by-step guide
3. Check `PROJECT_STRUCTURE.md` for architecture
4. Visit API docs: http://localhost:8000/docs

## What's Next?

- Customize UI colors and branding
- Add more QR code sizes (small, medium, large)
- Implement admin panel
- Add SMS notifications
- Create mobile app
- Add QR code analytics
- Implement QR code batches

---

**Happy coding! 🚀**

**Built by Gaurang Kothari (X Googler)**


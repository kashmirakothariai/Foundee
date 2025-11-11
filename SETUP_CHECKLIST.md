# ✅ Setup Checklist - Everything You Need

**Owner:** Gaurang Kothari (X Googler)

---

## 🎯 Quick Overview

You need to configure **3 main things**:
1. ✅ **Backend** (.env file)
2. ✅ **Frontend** (.env file)
3. ✅ **Database** (PostgreSQL)

---

## 📋 Step-by-Step Setup Guide

### ⚡ STEP 1: Backend Configuration

#### 1.1 Create `.env` File

```bash
cd backend
copy .env.example .env
```

#### 1.2 Edit `backend/.env` File

Open `backend/.env` in your editor and fill in these values:

```env
# ============================================
# 1. DATABASE CONFIGURATION (REQUIRED)
# ============================================
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/foundee_db
# Replace: YOUR_PASSWORD with your PostgreSQL password
# Example: postgresql://postgres:admin123@localhost:5432/foundee_db

# ============================================
# 2. SECURITY KEYS (REQUIRED)
# ============================================
SECRET_KEY=your-secret-key-minimum-32-characters-long-please-change-this
# This can be ANY random string, minimum 32 characters
# Example: abc123def456ghi789jkl012mno345pqr678stu901vwx234

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# 3. GOOGLE OAUTH (REQUIRED)
# ============================================
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
# Get this from: https://console.cloud.google.com/
# Example: 123456789-abcdefghijk.apps.googleusercontent.com

GOOGLE_CLIENT_SECRET=your-google-client-secret
# Get this from Google Cloud Console
# Example: GOCSPX-abc123def456ghi789

# ============================================
# 4. ENCRYPTION (OPTIONAL - for development set to false)
# ============================================
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=

# ============================================
# 5. FRONTEND URL (REQUIRED)
# ============================================
FRONTEND_URL=http://localhost:3000

# ============================================
# 6. EMAIL CONFIGURATION (REQUIRED for notifications)
# ============================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
# Replace with your Gmail address

SMTP_PASSWORD=abcd efgh ijkl mnop
# Use Gmail App Password (NOT your regular password!)
# Get from: https://myaccount.google.com/apppasswords
# Example: abcd efgh ijkl mnop (16 characters with spaces)
```

---

### ⚡ STEP 2: Frontend Configuration

#### 2.1 Create `.env` File

```bash
cd frontend
copy .env.example .env
```

#### 2.2 Edit `frontend/.env` File

Open `frontend/.env` and fill in:

```env
# ============================================
# 1. BACKEND API URL (REQUIRED)
# ============================================
REACT_APP_API_URL=http://localhost:8000

# ============================================
# 2. GOOGLE OAUTH CLIENT ID (REQUIRED)
# ============================================
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
# MUST BE THE SAME as backend GOOGLE_CLIENT_ID
# Example: 123456789-abcdefghijk.apps.googleusercontent.com
```

---

### ⚡ STEP 3: Get Google OAuth Credentials

#### 3.1 Go to Google Cloud Console

Open: https://console.cloud.google.com/

#### 3.2 Create/Select Project

1. Click dropdown at top → "New Project"
2. Project Name: **Foundee**
3. Click "Create"

#### 3.3 Enable Google+ API

1. Go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click it → Click "Enable"

#### 3.4 Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure consent screen:
   - User Type: **External**
   - App name: **Foundee**
   - User support email: **your email**
   - Developer contact: **your email**
   - Click "Save and Continue" (skip scopes, test users)

4. Create OAuth Client:
   - Application type: **Web application**
   - Name: **Foundee Web Client**
   
5. **Authorized JavaScript origins:**
   ```
   http://localhost:3000
   http://localhost:8000
   ```
   
6. **Authorized redirect URIs:**
   ```
   http://localhost:3000
   ```

7. Click "Create"

#### 3.5 Copy Credentials

You'll see a popup with:
- **Client ID** → Copy to both .env files
- **Client Secret** → Copy to backend/.env only

**Example:**
```
Client ID: 123456789-abcdefghijk.apps.googleusercontent.com
Client Secret: GOCSPX-abc123def456ghi789
```

---

### ⚡ STEP 4: Setup Gmail App Password (for Emails)

#### 4.1 Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification"
3. Click and enable it (follow steps)

#### 4.2 Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. App name: **Foundee**
3. Click "Create"
4. You'll get a 16-character password like: `abcd efgh ijkl mnop`
5. Copy this to `backend/.env` as `SMTP_PASSWORD`

**Important:** Use App Password, NOT your regular Gmail password!

---

### ⚡ STEP 5: Install PostgreSQL (if not installed)

#### 5.1 Check if PostgreSQL is Installed

```powershell
psql --version
```

If you see version number → Already installed ✅  
If error → Need to install ❌

#### 5.2 Install PostgreSQL (if needed)

Download from: https://www.postgresql.org/download/windows/

During installation:
- Remember the **password** you set for postgres user
- Default port: **5432** (keep it)

---

### ⚡ STEP 6: Create Database

#### 6.1 Create Database

```powershell
# Option 1: Using createdb command
createdb -U postgres foundee_db

# Option 2: Using psql
psql -U postgres
CREATE DATABASE foundee_db;
\q
```

**If prompted for password:** Enter the password you set during PostgreSQL installation

---

### ⚡ STEP 7: Install Backend Dependencies

#### 7.1 Create Virtual Environment

```powershell
cd backend
python -m venv venv
```

#### 7.2 Activate Virtual Environment

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat
```

#### 7.3 Install Python Packages

```powershell
pip install -r requirements.txt
```

**This installs:**
- FastAPI
- PostgreSQL driver
- SQLAlchemy
- Alembic
- Google Auth
- And more...

---

### ⚡ STEP 8: Run Database Migrations

```powershell
cd backend
# Make sure venv is activated
alembic upgrade head
```

**This creates all tables:**
- user_login
- user_dtls
- qr_dtls
- qr_usage

---

### ⚡ STEP 9: Install Frontend Dependencies

```powershell
cd frontend
npm install
```

**This installs:**
- React
- React Router
- Axios
- QR code libraries
- And more...

---

## 🚀 STEP 10: Start the Services!

### Method 1: Using Debug Mode (Recommended)

1. Press **F5** in Cursor/VS Code
2. Select **"🚀 Full Stack (Both Servers)"**
3. Wait 30 seconds
4. Open http://localhost:3000

### Method 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm start
```

---

## ✅ Verification Checklist

After starting, verify everything works:

### ✅ Backend Running?
```
Open: http://localhost:8000/docs
Should see: FastAPI documentation page
```

### ✅ Frontend Running?
```
Open: http://localhost:3000
Should see: Foundee login page
```

### ✅ Database Connected?
```powershell
psql -U postgres -d foundee_db -c "\dt"
Should show: 4 tables (user_login, user_dtls, qr_dtls, qr_usage)
```

### ✅ Google OAuth Working?
```
1. Click "Sign in with Google" button
2. Should open Google login popup
3. After login, should redirect to dashboard
```

---

## 📝 Summary - What You Need

### 🔑 Required Information:

| What | Where to Get | Where to Put |
|------|-------------|--------------|
| **PostgreSQL Password** | You set during install | `backend/.env` → `DATABASE_URL` |
| **Secret Key** | Generate random string (32+ chars) | `backend/.env` → `SECRET_KEY` |
| **Google Client ID** | Google Cloud Console | Both `.env` files |
| **Google Client Secret** | Google Cloud Console | `backend/.env` only |
| **Gmail Address** | Your Gmail | `backend/.env` → `SMTP_USER` |
| **Gmail App Password** | Google Account Settings | `backend/.env` → `SMTP_PASSWORD` |

---

## 🎯 Quick Reference - File Locations

```
Foundee/
├── backend/
│   ├── .env                  ← Configure this! (6 values needed)
│   ├── .env.example          ← Template to copy
│   ├── venv/                 ← Create with: python -m venv venv
│   └── requirements.txt      ← Install with: pip install -r requirements.txt
│
├── frontend/
│   ├── .env                  ← Configure this! (2 values needed)
│   ├── .env.example          ← Template to copy
│   ├── node_modules/         ← Create with: npm install
│   └── package.json          ← Lists all dependencies
│
└── .vscode/
    └── launch.json           ← Press F5 to use this
```

---

## 🚨 Common Issues

### Issue 1: "Module 'uvicorn' not found"
**Solution:** Activate venv and install requirements
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue 2: "Cannot connect to database"
**Solution:** Check DATABASE_URL in backend/.env
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/foundee_db
```

### Issue 3: "Google OAuth not working"
**Solution:** 
1. Check GOOGLE_CLIENT_ID matches in both .env files
2. Wait 5-10 minutes for Google changes to propagate
3. Clear browser cache

### Issue 4: "Emails not sending"
**Solution:** Use Gmail App Password (not regular password)
1. Enable 2FA: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use 16-character code in SMTP_PASSWORD

---

## 🎉 You're Ready!

Once you've completed all 10 steps, you can:

1. **Press F5** → Start both servers
2. **Open http://localhost:3000**
3. **Test the application!**

---

**Need help? Check these guides:**
- START_DEBUGGING.md - How to run with F5
- QUICK_DEBUG_GUIDE.md - Quick reference
- TROUBLESHOOTING.md - Common problems
- FLOW_SUMMARY.md - How the app works

---

**Built by Gaurang Kothari (X Googler)**


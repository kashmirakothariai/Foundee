# 🎯 Quick Reference Card

**Owner:** Gaurang Kothari (X Googler)

---

## 📝 What You Need (6 Things)

| # | What | Where to Get | Example |
|---|------|-------------|---------|
| 1 | **PostgreSQL Password** | Set during PG install | `admin123` |
| 2 | **Secret Key** | Generate random 32+ chars | `abc123xyz...` |
| 3 | **Google Client ID** | Google Cloud Console | `123-abc.apps.googleusercontent.com` |
| 4 | **Google Client Secret** | Google Cloud Console | `GOCSPX-abc123...` |
| 5 | **Gmail Address** | Your Gmail | `you@gmail.com` |
| 6 | **Gmail App Password** | Google Account Settings | `abcd efgh ijkl mnop` |

---

## 📂 Where to Put Them

### Backend `.env` (needs 6 values):
```
backend/.env

DATABASE_URL → Use #1 (PostgreSQL Password)
SECRET_KEY → Use #2 (Random string)
GOOGLE_CLIENT_ID → Use #3
GOOGLE_CLIENT_SECRET → Use #4
SMTP_USER → Use #5 (Gmail)
SMTP_PASSWORD → Use #6 (App Password)
```

### Frontend `.env` (needs 2 values):
```
frontend/.env

REACT_APP_API_URL → http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID → Use #3 (Same as backend!)
```

---

## 🚀 Setup Commands (Run Once)

```powershell
# 1. Create database
createdb -U postgres foundee_db

# 2. Setup backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env now!
alembic upgrade head

# 3. Setup frontend
cd ..\frontend
npm install
copy .env.example .env
# Edit .env now!
```

---

## ▶️ Start Commands (Every Time)

### Easy Way (Recommended):
```
Press F5 → Select "🚀 Full Stack (Both Servers)"
```

### Manual Way:
```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## 🔗 Access URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## ✅ Quick Test

```powershell
# Backend running?
curl http://localhost:8000/health

# Database working?
psql -U postgres -d foundee_db -c "\dt"

# Frontend?
# Open browser: http://localhost:3000
```

---

## 🔑 Get Google OAuth Credentials

1. Go to: https://console.cloud.google.com/
2. Create project: "Foundee"
3. Enable "Google+ API"
4. Create OAuth credentials
5. Add origins: `http://localhost:3000`, `http://localhost:8000`
6. Copy Client ID & Secret

---

## 📧 Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2FA (if not enabled)
3. Create app password: "Foundee"
4. Copy 16-character code
5. Use in SMTP_PASSWORD

---

## 🚨 Quick Fixes

| Problem | Solution |
|---------|----------|
| Port in use | `taskkill /PID <PID> /F` |
| Module not found | `pip install -r requirements.txt` |
| Database error | Check DATABASE_URL password |
| OAuth fails | Wait 5-10 mins, clear cache |
| Email fails | Use App Password, not regular |

---

## 📚 Full Guides

- **SETUP_CHECKLIST.md** ← Complete step-by-step
- **CONFIG_TEMPLATE.md** ← Copy-paste templates
- **START_DEBUGGING.md** ← How to press F5
- **FLOW_SUMMARY.md** ← How app works

---

**Built by Gaurang Kothari (X Googler)**


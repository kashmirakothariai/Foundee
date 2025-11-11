# 🚀 Quick Debug Guide - Start in 2 Minutes!

**Owner:** Gaurang Kothari (X Googler)

---

## ⚡ Super Quick Start

### Step 1: Press F5
Just press **F5** in Cursor!

### Step 2: Select Configuration
Choose: **"🚀 Full Stack (Both Servers)"**

### Step 3: Done! 🎉
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 🎯 Available Debug Configurations

When you press F5, you'll see three options:

1. **🚀 Full Stack (Both Servers)** ⭐ **Use This!**
   - Starts backend AND frontend together
   - Best for testing the complete app

2. **🐍 Backend (FastAPI)**
   - Only starts Python backend
   - Good for API testing

3. **⚛️ Frontend (React)**
   - Only starts React frontend
   - Good for UI development

---

## ⚠️ First Time? Do This Once:

### Quick Setup (5 minutes):

1. **Backend Setup:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your settings
```

2. **Database Setup:**
```bash
createdb foundee_db
cd backend
alembic upgrade head
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
copy .env.example .env
# Edit .env with your settings
```

---

## 🎮 How to Use

### Start Servers:
1. Press **F5**
2. Select **"🚀 Full Stack (Both Servers)"**
3. Wait ~30 seconds for both to start
4. Open browser to http://localhost:3000

### Stop Servers:
- Press **Shift+F5**
- Or click red square in debug toolbar

### Restart:
- Press **Shift+F5** (stop)
- Press **F5** (start)

---

## 🐛 Debug Features

### Backend Debugging:
- Click line numbers to set **breakpoints**
- Code execution pauses at breakpoints
- Inspect variables
- Step through code

### View Logs:
- Check **Terminal** tab at bottom
- You'll see two terminals:
  - One for Backend (Python)
  - One for Frontend (React)

---

## ✅ Quick Test

Once servers are running:

1. **Test Backend:**
   - Go to: http://localhost:8000/docs
   - Should see API documentation

2. **Test Frontend:**
   - Go to: http://localhost:3000
   - Should see Foundee login page

---

## 🎯 Test the Full Flow

### Test 1: Login
1. Open http://localhost:3000
2. Click "Sign in with Google"
3. Should login successfully

### Test 2: Create QR
1. Go to Dashboard
2. Click "Create New QR"
3. QR should appear

### Test 3: Scan QR
1. Click "Scan QR"
2. Use manual input with QR ID
3. Should show your details

---

## 💡 Pro Tips

### Tip 1: Auto-Reload
- Backend: Auto-reloads on Python file changes
- Frontend: Hot reload on React file changes
- No need to restart!

### Tip 2: Check Status
```bash
# Backend running?
curl http://localhost:8000/health

# Frontend running?
# Just open http://localhost:3000
```

### Tip 3: View Database
```bash
psql -d foundee_db
\dt  # List tables
SELECT * FROM user_login;
```

---

## 🚨 Common Issues

### Port Already in Use?
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Error?
1. Start PostgreSQL
2. Check .env DATABASE_URL
3. Run: `createdb foundee_db`

### Module Not Found?
```bash
# Backend
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## 🎉 That's It!

**Just press F5 and start testing your app!**

For detailed instructions, see: **RUN_INSTRUCTIONS.md**

---

**Built by Gaurang Kothari (X Googler)**


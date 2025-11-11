# ▶️ START DEBUGGING - Visual Guide

**Owner:** Gaurang Kothari (X Googler)

---

## 🎯 How to Start Both Servers

### Method 1: Keyboard Shortcut (Easiest)

```
Just Press: F5
```

That's it! 🎉

---

### Method 2: Using Menu

1. Click **Run** menu at top
2. Select **Start Debugging**
3. Choose **"🚀 Full Stack (Both Servers)"**

---

### Method 3: Debug Panel

1. Click Debug icon in left sidebar (▶️ with bug icon)
2. At top, select dropdown: **"🚀 Full Stack (Both Servers)"**
3. Click green play button ▶️

---

## 📋 What You'll See

### After Pressing F5:

```
Step 1: Debug Configuration Dropdown Appears
┌────────────────────────────────────┐
│ Select Configuration to Debug:    │
├────────────────────────────────────┤
│ 🚀 Full Stack (Both Servers)     │ ← Choose This!
│ 🐍 Backend (FastAPI)              │
│ ⚛️ Frontend (React)               │
└────────────────────────────────────┘
```

### Step 2: Terminals Open

You'll see two terminals at the bottom:

```
Terminal 1: Backend (FastAPI)
├─ Python activates
├─ Uvicorn starts
├─ Loads FastAPI app
└─ ✓ Listening on http://0.0.0.0:8000

Terminal 2: Frontend (React)
├─ npm start runs
├─ Webpack compiles
├─ React dev server starts
└─ ✓ Compiled successfully!
    On Your Network: http://localhost:3000
```

### Step 3: Ready!

```
✅ Backend:  http://localhost:8000
✅ Frontend: http://localhost:3000
✅ API Docs: http://localhost:8000/docs
```

---

## 🎮 Debug Toolbar

Once running, you'll see a debug toolbar at the top:

```
┌──────────────────────────────────────┐
│ ⏸ ⏹ ⟳ ⏯ ⬇ ➡ ↩               × │
└──────────────────────────────────────┘
  │  │  │  │
  │  │  │  └─ Play/Continue
  │  │  └──── Restart
  │  └─────── Stop (Shift+F5)
  └────────── Pause
```

---

## 🛑 How to Stop

### Three Ways:

1. **Keyboard:** Press **Shift+F5**
2. **Toolbar:** Click red square ⏹
3. **Menu:** Run → Stop Debugging

⚠️ **Important:** Stopping the compound config stops BOTH servers!

---

## 🔄 How to Restart

### Quick Restart:
1. Press **Shift+F5** (stop)
2. Press **F5** (start)

### Or use restart button:
- Click the restart button ⟳ in debug toolbar

---

## 📊 View Output

### Backend Logs:
```
Terminal → Backend
Shows:
- API requests
- Database queries
- Python print() statements
- Error messages
```

### Frontend Logs:
```
Terminal → Frontend
Shows:
- Compilation status
- npm warnings
- React warnings
- console.log() from browser
```

### API Logs:
```
Browser Console (F12)
Shows:
- Network requests
- console.log()
- React errors
```

---

## 🐛 Set Breakpoints

### In Python Files (Backend):

1. Open any Python file in `backend/app/`
2. Click left of line number (red dot appears)
3. When code hits that line, execution pauses
4. Inspect variables in Debug panel

Example:
```python
def scan_qr(qr_id: UUID):
    qr = db.query(QRDetails).filter(...).first()  # ← Click here
    # Execution will pause here when API is called
    return qr
```

### In React Files (Frontend):

Use `console.log()` and check browser console (F12):
```javascript
const handleScan = (qrId) => {
  console.log('Scanning QR:', qrId);  // Check browser console
};
```

---

## 🎯 Test After Starting

### 1. Check Backend is Running:

Open browser: http://localhost:8000/docs

Should see:
```
Foundee API
FastAPI automatic documentation
```

### 2. Check Frontend is Running:

Open browser: http://localhost:3000

Should see:
```
Foundee
QR-based Lost and Found
Sign in with Google button
```

### 3. Test Complete Flow:

1. Click "Sign in with Google"
2. Login with your account
3. Should reach Dashboard
4. Click "Create New QR"
5. QR should be created

**If all works → You're ready!** ✅

---

## 📍 File Locations

The files I created for you:

```
Foundee/
├── .vscode/
│   ├── launch.json          ← Debug configurations
│   └── settings.json        ← VS Code settings
├── START_DEBUGGING.md       ← This file
├── QUICK_DEBUG_GUIDE.md     ← Quick reference
└── RUN_INSTRUCTIONS.md      ← Detailed guide
```

---

## 🚨 Troubleshooting

### Configuration Not Appearing?

**Solution:**
1. Make sure you're in workspace folder
2. Close and reopen Cursor
3. Press F5 again

### Backend Won't Start?

**Check:**
- Is virtual environment created? `backend/venv/`
- Is .env configured? `backend/.env`
- Is PostgreSQL running?
- Are dependencies installed?

**Fix:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Won't Start?

**Check:**
- Is node_modules installed? `frontend/node_modules/`
- Is .env configured? `frontend/.env`

**Fix:**
```bash
cd frontend
npm install
```

### Port Already in Use?

**Error:** "EADDRINUSE: address already in use :::3000"

**Fix:**
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 💡 Next Steps

Once servers are running:

1. **Read:** FLOW_SUMMARY.md - Understand the complete flow
2. **Read:** ADMIN_FLOW_GUIDE.md - Learn admin features
3. **Test:** Follow test scenarios in QUICK_DEBUG_GUIDE.md
4. **Develop:** Make changes and see them live!

---

## 🎉 You're All Set!

### To Start Testing Now:

1. Press **F5**
2. Select **"🚀 Full Stack (Both Servers)"**
3. Wait 30 seconds
4. Open http://localhost:3000
5. Start testing!

**Happy coding!** 🚀

---

**Built by Gaurang Kothari (X Googler)**


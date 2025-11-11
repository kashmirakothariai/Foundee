# 🚀 How to Run Foundee in Cursor/VS Code

**Owner:** Gaurang Kothari (X Googler)

---

## ✨ Quick Start with Debug Mode

I've created a `launch.json` file that makes it super easy to run both servers!

---

## 🎯 Method 1: Run Both Servers at Once (Recommended)

### Steps:
1. **Press F5** or go to **Run → Start Debugging**
2. From the dropdown, select: **"🚀 Full Stack (Both Servers)"**
3. Both backend and frontend will start automatically!
4. Wait for both to be ready:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000

---

## 🎯 Method 2: Run Servers Individually

### Option A: Backend Only
1. Press **F5**
2. Select: **"🐍 Backend (FastAPI)"**
3. Backend will start on http://localhost:8000
4. API Docs: http://localhost:8000/docs

### Option B: Frontend Only
1. Press **F5**
2. Select: **"⚛️ Frontend (React)"**
3. Frontend will start on http://localhost:3000

---

## 📋 Before First Run - Setup Checklist

### ✅ Backend Setup

1. **Create `.env` file:**
   ```bash
   cd backend
   copy .env.example .env
   ```

2. **Edit `backend/.env`** with your settings:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/foundee_db
   SECRET_KEY=your-secret-key-here
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-secret
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

3. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   ```

4. **Activate and install dependencies:**
   ```bash
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Create database:**
   ```bash
   createdb foundee_db
   ```

6. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

### ✅ Frontend Setup

1. **Create `.env` file:**
   ```bash
   cd frontend
   copy .env.example .env
   ```

2. **Edit `frontend/.env`:**
   ```env
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

---

## 🎮 Using the Debug Configuration

### Available Configurations:

1. **🚀 Full Stack (Both Servers)**
   - Starts both backend and frontend
   - Best for full application testing
   - Both run in integrated terminal

2. **🐍 Backend (FastAPI)**
   - Only starts Python/FastAPI backend
   - Port: 8000
   - Supports Python debugging/breakpoints

3. **⚛️ Frontend (React)**
   - Only starts React development server
   - Port: 3000
   - Hot reload enabled

---

## 🐛 Debugging Features

### Backend (Python) Debugging:
- Set breakpoints in Python files
- Inspect variables
- Step through code
- View call stack
- Debug console available

### Frontend (React) Debugging:
- Console logs in terminal
- Hot reload on file changes
- Browser DevTools (F12)

---

## 🎯 Access Points After Starting

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React application |
| Backend API | http://localhost:8000 | FastAPI endpoints |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API ReDoc | http://localhost:8000/redoc | Alternative docs |

---

## 🛑 Stopping the Servers

### In Cursor/VS Code:
- Click the **Stop** button (red square) in the debug toolbar
- Or press **Shift+F5**
- Compound configuration stops both servers at once

### Manual Stop:
- Backend: **Ctrl+C** in backend terminal
- Frontend: **Ctrl+C** in frontend terminal

---

## 🔄 Restarting Servers

### With Debug Mode:
1. Stop with **Shift+F5**
2. Start again with **F5**

### Backend Auto-Reload:
- Backend uses `--reload` flag
- Automatically restarts on Python file changes
- No need to manually restart

### Frontend Hot Reload:
- React has built-in hot reload
- Changes appear instantly in browser
- No restart needed

---

## 📝 Troubleshooting

### Port Already in Use

**Error:** "Address already in use" on port 8000 or 3000

**Solution:**
```powershell
# Find and kill process on port 8000 (backend)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Find and kill process on port 3000 (frontend)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Virtual Environment Not Found

**Error:** Python virtual environment not found

**Solution:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Node Modules Missing

**Error:** Cannot find module errors in frontend

**Solution:**
```bash
cd frontend
npm install
```

### Database Connection Error

**Error:** Cannot connect to PostgreSQL

**Solution:**
1. Start PostgreSQL service
2. Verify DATABASE_URL in `backend/.env`
3. Create database: `createdb foundee_db`
4. Run migrations: `alembic upgrade head`

### Python Extension Not Installed

**Error:** Debug configuration won't work

**Solution:**
1. Install Python extension: `ms-python.python`
2. Restart Cursor/VS Code

---

## 💡 Pro Tips

### Tip 1: View Logs
- Backend logs appear in **Terminal** tab
- Frontend logs in browser console (F12)
- Both show in integrated terminal

### Tip 2: Multiple Terminals
- Cursor opens separate terminals for each server
- Easy to see logs from both
- Can run commands in either

### Tip 3: Breakpoint Debugging
```python
# In any Python file (backend)
def some_function():
    x = 10  # Click left of line number to set breakpoint
    y = x * 2  # Execution will pause here
    return y
```

### Tip 4: Environment Variables
- Backend reads from `backend/.env`
- Frontend reads from `frontend/.env`
- Changes require restart

### Tip 5: Quick Test Backend
```bash
# Test if backend is running
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

## 🚀 Ready to Go!

### To Start Testing:

1. **First Time Setup:**
   - Run setup script: `setup.bat`
   - Configure `.env` files
   - Create database
   - Run migrations

2. **Every Time After:**
   - Just press **F5**
   - Select **"🚀 Full Stack (Both Servers)"**
   - Start testing!

---

## 📚 What to Test

### Test Flow 1: Create QR (Admin)
1. Login with Google
2. Go to Dashboard
3. Click "Create New QR"
4. Download QR image

### Test Flow 2: Claim QR (First User)
1. Scan/open QR URL
2. See "Unclaimed QR" message
3. Click "Claim This QR Code"
4. Login with Google
5. Add your details
6. Set permissions
7. Save

### Test Flow 3: Owner Edits
1. Scan your own QR
2. Should auto-open edit panel
3. Update details
4. Change permissions
5. Save

### Test Flow 4: Others View
1. Open incognito window
2. Scan QR (no login)
3. See filtered contact info
4. Owner gets email notification

---

## 🎉 Happy Testing!

Everything is set up for easy debugging and testing. Just press F5 and you're ready to go!

**Built by Gaurang Kothari (X Googler)**


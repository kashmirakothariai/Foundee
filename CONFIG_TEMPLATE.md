# 📝 Configuration Templates - Copy & Paste Ready

**Owner:** Gaurang Kothari (X Googler)

---

## 🎯 Quick Config - Fill in the Blanks

### 1️⃣ Backend Configuration (`backend/.env`)

```env
# DATABASE
DATABASE_URL=postgresql://postgres:YOUR_DB_PASSWORD_HERE@localhost:5432/foundee_db

# SECURITY
SECRET_KEY=GENERATE_RANDOM_32_CHARS_HERE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GOOGLE OAUTH
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE

# ENCRYPTION (leave as false for development)
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=

# FRONTEND
FRONTEND_URL=http://localhost:3000

# EMAIL
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=YOUR_EMAIL@gmail.com
SMTP_PASSWORD=YOUR_16_CHAR_APP_PASSWORD_HERE
```

---

### 2️⃣ Frontend Configuration (`frontend/.env`)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
```

---

## 🔑 What Each Value Means

### DATABASE_URL
```
Format: postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE
Example: postgresql://postgres:admin123@localhost:5432/foundee_db
```

**Fill in:**
- `USERNAME` → Usually `postgres`
- `PASSWORD` → Your PostgreSQL password
- `HOST` → `localhost` (if running locally)
- `PORT` → `5432` (default PostgreSQL port)
- `DATABASE` → `foundee_db`

---

### SECRET_KEY
```
Any random string, minimum 32 characters
Example: abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567
```

**Generate one:**
```python
# Python method
import secrets
print(secrets.token_urlsafe(32))
```

Or just type random characters:
```
asdfghjklqwertyuiopzxcvbnm123456789
```

---

### GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET

**Get from:** https://console.cloud.google.com/

**Format:**
```
Client ID: 123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com
Client Secret: GOCSPX-abcdefghijklmnopqrstuvwx
```

**Steps:**
1. Create project in Google Cloud Console
2. Enable Google+ API
3. Create OAuth 2.0 credentials
4. Copy Client ID → Put in BOTH .env files
5. Copy Client Secret → Put in backend/.env ONLY

---

### SMTP_USER & SMTP_PASSWORD

**SMTP_USER:**
```
Your Gmail address
Example: john.doe@gmail.com
```

**SMTP_PASSWORD:**
```
16-character App Password (NOT your regular Gmail password!)
Example: abcd efgh ijkl mnop
```

**Get App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2FA first if not enabled
3. Create app password named "Foundee"
4. Copy the 16-character code

---

## 📋 Example Filled Configuration

### Example `backend/.env`

```env
# DATABASE
DATABASE_URL=postgresql://postgres:mySecurePass123@localhost:5432/foundee_db

# SECURITY
SECRET_KEY=xyz789abc123def456ghi789jkl012mno345pqr678

# GOOGLE OAUTH
GOOGLE_CLIENT_ID=123456789012-abcdefghijk.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456ghi789jkl012

# ENCRYPTION
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=

# FRONTEND
FRONTEND_URL=http://localhost:3000

# EMAIL
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=gaurang.kothari@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
```

---

### Example `frontend/.env`

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=123456789012-abcdefghijk.apps.googleusercontent.com
```

---

## ✅ Validation Checklist

Before starting servers, verify:

- [ ] `backend/.env` exists and has 10 values filled
- [ ] `frontend/.env` exists and has 2 values filled
- [ ] GOOGLE_CLIENT_ID is same in both files
- [ ] DATABASE_URL password matches your PostgreSQL password
- [ ] SMTP_PASSWORD is App Password (16 chars with spaces)
- [ ] Database `foundee_db` is created
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Migrations run (`alembic upgrade head`)

---

## 🚀 Ready to Start?

Once all values are filled:

```bash
# Press F5 in Cursor/VS Code
# Or run manually:

# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## 🎯 Quick Test

After starting, test each component:

**1. Backend:**
```
http://localhost:8000/health
Should return: {"status":"healthy"}
```

**2. Frontend:**
```
http://localhost:3000
Should show: Foundee login page
```

**3. Database:**
```powershell
psql -U postgres -d foundee_db -c "SELECT COUNT(*) FROM qr_dtls;"
Should work without errors
```

**4. Google OAuth:**
```
Click "Sign in with Google"
Should open Google login popup
```

---

## 🎉 You're All Set!

Configuration complete! Now you can:
- Press F5 to start
- Open http://localhost:3000
- Test the application

---

**Built by Gaurang Kothari (X Googler)**


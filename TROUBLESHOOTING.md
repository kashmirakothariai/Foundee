# Foundee - Troubleshooting Guide

**Owner:** Gaurang Kothari (X Googler)

Common issues and their solutions.

---

## 🔧 Installation Issues

### Python Virtual Environment Won't Create

**Problem:** `python -m venv venv` fails

**Solutions:**
```bash
# Windows
python -m pip install --upgrade pip
python -m venv venv

# Linux/Mac
sudo apt install python3-venv
python3 -m venv venv
```

### pip install fails

**Problem:** Can't install requirements.txt

**Solutions:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Try installing packages individually
pip install fastapi uvicorn sqlalchemy
```

### npm install fails

**Problem:** Frontend dependencies won't install

**Solutions:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and lock file
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Or use yarn
npm install -g yarn
yarn install
```

---

## 🗄️ Database Issues

### Can't connect to PostgreSQL

**Problem:** `could not connect to server`

**Solutions:**
```bash
# Check if PostgreSQL is running
# Windows
net start postgresql

# Linux
sudo service postgresql status
sudo service postgresql start

# Mac
brew services list
brew services start postgresql
```

### Database doesn't exist

**Problem:** `database "foundee_db" does not exist`

**Solutions:**
```bash
# Create database
createdb -U postgres foundee_db

# Or via psql
psql -U postgres
CREATE DATABASE foundee_db;
\q
```

### Permission denied for database

**Problem:** `permission denied for database`

**Solutions:**
```sql
-- Connect as superuser
psql -U postgres

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE foundee_db TO your_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;
```

### Alembic migration fails

**Problem:** `alembic upgrade head` fails

**Solutions:**
```bash
# Check alembic version
alembic current

# Reset alembic (WARNING: drops all tables)
alembic downgrade base
alembic upgrade head

# Create fresh migration
alembic revision --autogenerate -m "Initial"
alembic upgrade head

# Check for errors in migration file
# backend/alembic/versions/*.py
```

---

## 🚀 Backend Issues

### Port 8000 already in use

**Problem:** `Address already in use`

**Solutions:**
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solutions:**
```bash
# Make sure you're in backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Import errors

**Problem:** `ImportError: cannot import name 'X'`

**Solutions:**
```bash
# Reinstall problematic package
pip uninstall package_name
pip install package_name

# Check package version
pip show package_name

# Reinstall all
pip install -r requirements.txt --force-reinstall
```

### pydantic validation errors

**Problem:** `ValidationError: X field required`

**Solutions:**
- Check request body matches schema
- Verify .env file has all required variables
- Check API request includes all required fields
- Review backend/app/schemas.py for required fields

---

## ⚛️ Frontend Issues

### Port 3000 already in use

**Problem:** `Port 3000 is already in use`

**Solutions:**
```bash
# Find and kill process
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>

# Or use different port
PORT=3001 npm start
```

### React won't start

**Problem:** `npm start` fails

**Solutions:**
```bash
# Clear cache
rm -rf node_modules .cache

# Reinstall
npm install

# Clear npm cache
npm cache clean --force

# Try different node version
nvm install 16
nvm use 16
```

### Module not found errors

**Problem:** `Module not found: Can't resolve 'X'`

**Solutions:**
```bash
# Install missing package
npm install package-name

# Check package.json for missing dependencies
npm install

# Verify imports use correct paths
# Should be: import X from './components/X'
# Not: import X from 'components/X'
```

### CORS errors

**Problem:** `Access-Control-Allow-Origin` error

**Solutions:**
```python
# Check backend/app/main.py CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Blank white screen

**Problem:** React app shows blank page

**Solutions:**
```bash
# Check browser console for errors
# Press F12 → Console tab

# Check if API is running
curl http://localhost:8000/health

# Rebuild
rm -rf node_modules build
npm install
npm start
```

---

## 🔐 Authentication Issues

### Google OAuth not working

**Problem:** Google login fails

**Solutions:**

1. **Verify Client ID:**
```bash
# Check both .env files have same Client ID
cat backend/.env | grep GOOGLE_CLIENT_ID
cat frontend/.env | grep REACT_APP_GOOGLE_CLIENT_ID
```

2. **Check Google Console:**
- Go to https://console.cloud.google.com
- Verify Authorized JavaScript origins include:
  - `http://localhost:3000`
  - `http://localhost:8000`
- Authorized redirect URIs include:
  - `http://localhost:3000`

3. **Clear browser data:**
- Clear cookies and cache
- Try incognito mode

4. **Wait for propagation:**
- Changes in Google Console take 5-10 minutes

### JWT token expired

**Problem:** `Token expired` error

**Solutions:**
```bash
# Logout and login again
# Or increase expiration in backend/.env
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Restart backend
```

### 401 Unauthorized

**Problem:** API returns 401

**Solutions:**
```javascript
// Check localStorage has token
console.log(localStorage.getItem('token'));

// If missing, login again

// Check token is sent in headers
// frontend/src/utils/api.js should have:
headers: {
  Authorization: `Bearer ${token}`
}
```

---

## 📧 Email Issues

### Emails not sending

**Problem:** QR scan emails not received

**Solutions:**

1. **Use Gmail App Password:**
```bash
# Don't use regular password
# Generate App Password:
# 1. Enable 2FA on Gmail
# 2. Google Account → Security → App passwords
# 3. Select "Mail" and generate
# 4. Use 16-digit password in SMTP_PASSWORD
```

2. **Check SMTP settings:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=16-digit-app-password
```

3. **Test SMTP connection:**
```python
# Test with Python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email', 'app-password')
print("Success!")
```

4. **Check spam folder**

---

## 📱 QR Code Issues

### QR Scanner not working

**Problem:** Camera won't activate

**Solutions:**

1. **Check browser permissions:**
- Chrome: Settings → Privacy → Site Settings → Camera
- Allow camera access for localhost

2. **Use HTTPS in production:**
- Camera requires HTTPS (except localhost)

3. **Try different browser:**
- Chrome works best
- Firefox, Safari also supported

4. **Check console errors:**
- Press F12 → Console
- Look for camera permission errors

### QR Code won't scan

**Problem:** QR code not recognized

**Solutions:**

1. **Check QR quality:**
- Ensure good lighting
- Hold camera steady
- Move camera closer/farther

2. **Try manual input:**
- Copy QR ID from URL
- Use "Enter QR Code ID manually" option

3. **Verify QR format:**
- Should be: `http://localhost:3000/qr/{uuid}`
- Check QR was generated correctly

### QR Image won't download

**Problem:** Download button doesn't work

**Solutions:**
```javascript
// Check browser console for errors
// Verify qrcode library is installed
npm list qrcode

// Reinstall if needed
npm install qrcode
```

---

## 🌐 Network Issues

### API calls failing

**Problem:** Frontend can't reach backend

**Solutions:**

1. **Verify backend is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

2. **Check REACT_APP_API_URL:**
```bash
cat frontend/.env
# Should be: REACT_APP_API_URL=http://localhost:8000
```

3. **Check network tab:**
- Press F12 → Network
- See if requests are being made
- Check request/response

### Timeout errors

**Problem:** Requests timing out

**Solutions:**
- Check backend is running
- Increase timeout in axios config
- Check firewall settings
- Verify database connection

---

## 🐛 Common Errors

### "Cannot read property 'X' of undefined"

**Solutions:**
```javascript
// Use optional chaining
user?.name instead of user.name

// Add null checks
if (user && user.name) { ... }

// Provide defaults
const name = user?.name || 'Unknown';
```

### "Key prop missing" warning

**Solutions:**
```javascript
// Add key prop to lists
{items.map(item => (
  <div key={item.id}>...</div>
))}
```

### SQLAlchemy "No such table" error

**Solutions:**
```bash
# Run migrations
cd backend
alembic upgrade head

# Or recreate database
dropdb foundee_db
createdb foundee_db
alembic upgrade head
```

---

## 🔍 Debugging Tips

### Enable debug mode

**Backend:**
```python
# backend/app/main.py
app = FastAPI(debug=True)

# Run with log level
uvicorn app.main:app --reload --log-level debug
```

**Frontend:**
```javascript
// Add console.logs
console.log('User data:', user);
console.log('API response:', response);
```

### Check logs

**Backend:**
```bash
# Terminal where uvicorn is running shows logs
# Add print statements for debugging
print(f"Debug: {variable}")
```

**Frontend:**
```bash
# Browser console (F12)
# Network tab for API calls
# React DevTools extension
```

### Database inspection

```bash
# Connect to database
psql -U postgres -d foundee_db

# List tables
\dt

# View table contents
SELECT * FROM user_login;
SELECT * FROM qr_dtls;

# Check relationships
\d+ user_login
```

---

## 📞 Still Having Issues?

If you're still stuck:

1. **Check Documentation:**
   - README.md - Main documentation
   - SETUP_INSTRUCTIONS.md - Setup guide
   - APPLICATION_FLOW.md - How it works

2. **Review Code:**
   - Check backend logs
   - Check browser console
   - Review API documentation: http://localhost:8000/docs

3. **Fresh Start:**
   ```bash
   # Complete reset
   dropdb foundee_db
   createdb foundee_db
   cd backend && alembic upgrade head
   cd ../frontend && rm -rf node_modules && npm install
   ```

4. **System Requirements:**
   - Python 3.9+
   - Node.js 16+
   - PostgreSQL 13+
   - Modern browser (Chrome, Firefox, Safari, Edge)

---

**Remember:** Most issues are configuration-related. Double-check your .env files!

**Built by Gaurang Kothari (X Googler)**


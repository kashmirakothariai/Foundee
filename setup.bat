@echo off
echo ================================
echo Foundee Setup Script (Windows)
echo Owner: Gaurang Kothari (X Googler)
echo ================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo All prerequisites are installed
echo.

:: Backend Setup
echo Setting up Backend...
cd backend

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

:: Copy environment file
if not exist .env (
    copy .env.example .env
    echo Please configure backend\.env file with your credentials
)

echo Backend setup complete
echo.

:: Frontend Setup
echo Setting up Frontend...
cd ..\frontend

:: Install dependencies
call npm install

:: Copy environment file
if not exist .env (
    copy .env.example .env
    echo Please configure frontend\.env file with your Google Client ID
)

echo Frontend setup complete
echo.

cd ..

echo ================================
echo Setup Complete!
echo.
echo Next steps:
echo 1. Configure backend\.env with your credentials
echo 2. Configure frontend\.env with your Google Client ID
echo 3. Create PostgreSQL database 'foundee_db'
echo 4. Run migrations: cd backend ^&^& venv\Scripts\activate ^&^& alembic revision --autogenerate -m "Initial" ^&^& alembic upgrade head
echo 5. Start backend: cd backend ^&^& uvicorn app.main:app --reload
echo 6. Start frontend: cd frontend ^&^& npm start
echo.
echo See README.md for detailed instructions
echo ================================
pause


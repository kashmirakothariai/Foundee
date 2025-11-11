#!/bin/bash

echo "🚀 Foundee Setup Script"
echo "Owner: Gaurang Kothari (X Googler)"
echo "=================================="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. Please install it first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed. Please install it first."
    exit 1
fi

echo "✅ All prerequisites are installed"
echo ""

# Backend Setup
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please configure backend/.env file with your credentials"
fi

echo "✅ Backend setup complete"
echo ""

# Frontend Setup
echo "📦 Setting up Frontend..."
cd ../frontend

# Install dependencies
npm install

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please configure frontend/.env file with your Google Client ID"
fi

echo "✅ Frontend setup complete"
echo ""

# Database Setup
echo "📦 Setting up Database..."
cd ..

# Create database (modify credentials as needed)
echo "Please enter your PostgreSQL username (default: postgres):"
read -r PG_USER
PG_USER=${PG_USER:-postgres}

createdb -U "$PG_USER" foundee_db 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Database 'foundee_db' created successfully"
else
    echo "⚠️  Database might already exist or check your PostgreSQL credentials"
fi

echo ""
echo "=================================="
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Configure backend/.env with your credentials"
echo "2. Configure frontend/.env with your Google Client ID"
echo "3. Run migrations: cd backend && source venv/bin/activate && alembic revision --autogenerate -m 'Initial' && alembic upgrade head"
echo "4. Start backend: cd backend && uvicorn app.main:app --reload"
echo "5. Start frontend: cd frontend && npm start"
echo ""
echo "📖 See README.md for detailed instructions"
echo "=================================="


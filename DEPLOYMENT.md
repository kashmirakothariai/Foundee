# Foundee - Deployment Guide

**Owner:** Gaurang Kothari (X Googler)

## Deployment Options

### Option 1: Traditional VPS (DigitalOcean, Linode, AWS EC2)

#### Prerequisites
- Ubuntu 20.04+ server
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt)

#### Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Python 3.9+
sudo apt install python3.9 python3.9-venv python3-pip -y

# Install Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs -y

# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
```

#### Database Setup

```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE foundee_db;
CREATE USER foundee_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE foundee_db TO foundee_user;
\q
```

#### Backend Deployment

```bash
# Clone repository
cd /var/www
sudo git clone https://github.com/yourusername/foundee.git
cd foundee/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
sudo nano .env
# Set production values

# Run migrations
alembic upgrade head

# Create systemd service
sudo nano /etc/systemd/system/foundee-backend.service
```

**foundee-backend.service:**
```ini
[Unit]
Description=Foundee FastAPI Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/foundee/backend
Environment="PATH=/var/www/foundee/backend/venv/bin"
ExecStart=/var/www/foundee/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable foundee-backend
sudo systemctl start foundee-backend
sudo systemctl status foundee-backend
```

#### Frontend Deployment

```bash
cd /var/www/foundee/frontend

# Install dependencies
npm install

# Configure .env
nano .env
# Set production values
# REACT_APP_API_URL=https://api.yourdomain.com

# Build production bundle
npm run build

# Copy build to nginx directory
sudo cp -r build/* /var/www/html/foundee/
```

#### Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/foundee
```

**foundee nginx config:**
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /var/www/html/foundee;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        alias /var/www/html/foundee/static/;
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/foundee /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### SSL Certificate

```bash
# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### Option 2: Heroku Deployment

#### Backend (Heroku)

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
cd backend
heroku create foundee-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GOOGLE_CLIENT_ID=your-client-id
heroku config:set GOOGLE_CLIENT_SECRET=your-secret
heroku config:set SMTP_USER=your-email
heroku config:set SMTP_PASSWORD=your-password
heroku config:set FRONTEND_URL=https://foundee-frontend.herokuapp.com

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run alembic upgrade head
```

#### Frontend (Netlify/Vercel)

**Netlify:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
cd frontend
npm run build

# Deploy
netlify deploy --prod --dir=build

# Set environment variables in Netlify dashboard
REACT_APP_API_URL=https://foundee-backend.herokuapp.com
REACT_APP_GOOGLE_CLIENT_ID=your-client-id
```

### Option 3: Docker Deployment

#### Create Dockerfiles

**backend/Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**frontend/Dockerfile:**
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: foundee_db
      POSTGRES_USER: foundee_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://foundee_user:secure_password@db:5432/foundee_db
      SECRET_KEY: your-secret-key
      GOOGLE_CLIENT_ID: your-client-id
      GOOGLE_CLIENT_SECRET: your-secret
      FRONTEND_URL: http://localhost:3000
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    environment:
      REACT_APP_API_URL: http://localhost:8000
      REACT_APP_GOOGLE_CLIENT_ID: your-client-id
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

```bash
# Deploy with Docker Compose
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

## Production Checklist

### Security
- [ ] Set strong SECRET_KEY (32+ characters)
- [ ] Enable ENCRYPTION_ENABLED=true
- [ ] Use HTTPS/SSL certificates
- [ ] Configure CORS for production domains only
- [ ] Use production database credentials
- [ ] Enable firewall (ufw/iptables)
- [ ] Set up regular database backups
- [ ] Use environment variables (never commit .env)
- [ ] Update Google OAuth redirect URIs
- [ ] Use production SMTP credentials

### Performance
- [ ] Enable database connection pooling
- [ ] Configure CDN for static files
- [ ] Enable gzip compression in nginx
- [ ] Set up database indexes
- [ ] Configure caching headers
- [ ] Use production build for React
- [ ] Optimize images and assets
- [ ] Enable database query optimization

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Configure uptime monitoring
- [ ] Set up database monitoring
- [ ] Enable application metrics
- [ ] Configure alerts
- [ ] Set up log rotation

### Backup
- [ ] Daily database backups
- [ ] Backup encryption
- [ ] Off-site backup storage
- [ ] Test restore procedures
- [ ] Document backup process

## Environment Variables (Production)

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:5432/foundee_db
SECRET_KEY=generate-secure-32-character-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-secret

ENCRYPTION_ENABLED=true
ENCRYPTION_KEY=generate-with-fernet-key

FRONTEND_URL=https://yourdomain.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_GOOGLE_CLIENT_ID=your-production-client-id
```

## Post-Deployment

### Test checklist
- [ ] Homepage loads
- [ ] Google OAuth works
- [ ] QR creation works
- [ ] QR scanning works
- [ ] Email notifications work
- [ ] Detail updates work
- [ ] Permission changes work
- [ ] Mobile responsive
- [ ] HTTPS working
- [ ] Database migrations applied

### Google OAuth Update
1. Go to Google Cloud Console
2. Update Authorized JavaScript origins:
   - https://yourdomain.com
   - https://api.yourdomain.com
3. Update Authorized redirect URIs:
   - https://yourdomain.com
4. Wait 5-10 minutes for changes to propagate

## Troubleshooting

### Backend not starting
```bash
# Check logs
sudo journalctl -u foundee-backend -f

# Check if port is in use
sudo lsof -i :8000
```

### Database connection error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U foundee_user -d foundee_db
```

### Nginx errors
```bash
# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Test configuration
sudo nginx -t
```

## Scaling

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Multiple backend instances
- Shared PostgreSQL database
- Redis for session storage

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add database indexes
- Enable caching

## Maintenance

### Database Backups
```bash
# Backup
pg_dump -U foundee_user foundee_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U foundee_user foundee_db < backup_20250102.sql
```

### Update Application
```bash
# Pull latest code
cd /var/www/foundee
sudo git pull

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart foundee-backend

# Frontend
cd ../frontend
npm install
npm run build
sudo cp -r build/* /var/www/html/foundee/
```

---

**Built by Gaurang Kothari (X Googler)**


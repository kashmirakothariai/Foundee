# Foundee - Feature List

**Owner:** Gaurang Kothari (X Googler)

## Core Features

### 🔐 Authentication & Authorization

- **Google OAuth 2.0 Integration**
  - One-click sign-in with Google
  - No password management required
  - Automatic user registration
  - Secure token-based sessions

- **JWT Token Authentication**
  - Stateless authentication
  - Configurable expiration (default 30 minutes)
  - Automatic token refresh
  - Secure token storage

- **Role-Based Access**
  - ASP Admin: Full access to all data
  - User: Access to own data only
  - Public: QR scanning without login

### 📱 QR Code Management

- **QR Code Generation**
  - Create unlimited QR codes
  - Unique UUID for each QR
  - High-quality PNG export
  - Configurable size (currently 300x300px)
  - Print-ready format

- **QR Code Scanning**
  - Camera-based scanning
  - Manual ID input option
  - No login required for viewing
  - Cross-platform compatibility
  - Works on mobile and desktop

- **QR Code Binding**
  - Bind QR to user account
  - Support for unbound QRs
  - One-time binding (cannot rebind)
  - Automatic binding on first scan by owner

### 👤 User Profile Management

- **Personal Information**
  - First Name
  - Last Name
  - Mobile Number
  - Email Address
  - Physical Address
  - Blood Group
  - Company Name
  - Additional Description

- **Profile Editing**
  - Real-time updates
  - Form validation
  - Success/error notifications
  - Mobile-responsive interface

### 🔒 Granular Privacy Controls

- **Field-Level Permissions**
  - Control visibility of each field independently
  - Toggle on/off for 8 different fields:
    - First Name visibility
    - Last Name visibility
    - Mobile Number visibility
    - Address visibility
    - Email visibility
    - Blood Group visibility
    - Company Name visibility
    - Description visibility

- **Real-Time Permission Updates**
  - Change visibility anytime
  - No effect on stored data
  - Instant application on next scan
  - Visual indicators for visibility status

### 📍 Location Tracking

- **Automatic Location Capture**
  - GPS coordinates on scan
  - Browser-based geolocation
  - Optional (user can deny)
  - Latitude and longitude storage

- **Location History**
  - Track all QR scans
  - View scan timestamps
  - Geographic data for each scan
  - Useful for lost item recovery

### 📧 Email Notifications

- **Real-Time Alerts**
  - Email sent on every QR scan
  - Includes scan location
  - Google Maps link
  - Timestamp of scan
  - QR ID reference

- **Email Service**
  - SMTP integration
  - Gmail support
  - Configurable SMTP server
  - App password support
  - Secure TLS connection

### 🎨 User Interface

- **Modern Design**
  - Beautiful gradient backgrounds
  - Card-based layouts
  - Smooth animations
  - Hover effects
  - Professional styling

- **Responsive Layout**
  - Mobile-first design
  - Tablet optimization
  - Desktop support
  - Touch-friendly buttons
  - Adaptive grids

- **User Experience**
  - Intuitive navigation
  - Clear call-to-actions
  - Loading states
  - Error messages
  - Success confirmations

### 🗄️ Database Features

- **PostgreSQL Database**
  - ACID compliance
  - Relational data integrity
  - UUID primary keys
  - Foreign key constraints
  - Indexed queries

- **Alembic Migrations**
  - Version control for schema
  - Automated migrations
  - Rollback capability
  - Database versioning
  - Team collaboration

- **Data Tracking**
  - Created timestamp
  - Updated timestamp
  - Created by user ID
  - Updated by user ID
  - Active/inactive flags

### 🔐 Security Features

- **End-to-End Encryption** (Optional)
  - Flag-based encryption
  - Fernet encryption algorithm
  - Configurable encryption key
  - Development mode (disabled)
  - Production mode (enabled)

- **SQL Injection Prevention**
  - ORM-based queries
  - Parameterized statements
  - Input validation
  - Pydantic schemas

- **CORS Protection**
  - Configurable origins
  - Credential support
  - Method restrictions
  - Header controls

- **Password Security**
  - Bcrypt hashing
  - Salt generation
  - Optional passwords (OAuth users)
  - Secure storage

## API Features

### 📚 Automatic Documentation

- **Swagger UI** (`/docs`)
  - Interactive API testing
  - Request/response examples
  - Schema definitions
  - Try it out functionality

- **ReDoc** (`/redoc`)
  - Alternative documentation
  - Better for reading
  - Organized by tags
  - Download OpenAPI spec

### 🚀 RESTful API

- **Standard HTTP Methods**
  - GET: Retrieve data
  - POST: Create resources
  - PUT: Update resources
  - DELETE: Remove resources (soft delete)

- **JSON Format**
  - All requests/responses in JSON
  - Consistent structure
  - Error details
  - Validation messages

### 🔄 API Versioning

- **Prefix-based versioning**
  - `/api/auth/*`
  - `/api/user/*`
  - `/api/qr/*`

## Dashboard Features

### 📊 User Dashboard

- **QR Code Gallery**
  - Grid view of all QRs
  - Visual QR previews
  - Quick actions per QR
  - Download buttons
  - Edit buttons

- **Quick Actions**
  - Create new QR
  - Scan QR code
  - Update details
  - View profile
  - Logout

- **Statistics** (Future)
  - Total QRs created
  - Total scans
  - Recent activity
  - Popular QRs

### 🔍 QR Scanner Interface

- **Camera Integration**
  - Live camera preview
  - Auto-detection
  - Manual capture
  - Permission handling
  - Error recovery

- **Manual Input**
  - Text input for QR ID
  - Copy-paste support
  - Validation
  - Direct navigation

### ✏️ Update Panel

- **Split View**
  - Left: Input fields
  - Right: Visibility toggles
  - Clear labels
  - Responsive layout

- **Form Features**
  - Auto-save (on submit)
  - Validation
  - Error messages
  - Success feedback
  - Cancel option

## Technical Features

### ⚡ Performance

- **Fast API Framework**
  - Async support
  - High performance
  - Automatic validation
  - Type hints

- **Database Optimization**
  - Connection pooling
  - Indexed queries
  - Efficient joins
  - Query optimization

### 🧪 Development Tools

- **Hot Reload**
  - Backend: Uvicorn --reload
  - Frontend: React hot module replacement
  - Instant updates
  - No restart needed

- **Environment Variables**
  - .env files
  - Separate dev/prod configs
  - Sensitive data protection
  - Easy configuration

### 📦 Package Management

- **Backend**
  - requirements.txt
  - Virtual environment
  - Version pinning
  - Easy installation

- **Frontend**
  - package.json
  - npm/yarn support
  - Lock files
  - Dependency management

## Future Enhancements (Not Implemented)

- [ ] Admin Dashboard
- [ ] QR Code Analytics
- [ ] Bulk QR Generation
- [ ] SMS Notifications
- [ ] Multiple QR Sizes
- [ ] Custom QR Designs
- [ ] QR Code Categories
- [ ] Social Media Integration
- [ ] Mobile App (React Native)
- [ ] Multi-language Support
- [ ] Dark Mode
- [ ] Export User Data
- [ ] Two-Factor Authentication
- [ ] Rate Limiting
- [ ] API Keys for Developers
- [ ] Webhook Integration
- [ ] Payment Integration (for premium features)
- [ ] QR Code Expiration
- [ ] Temporary QR Codes
- [ ] QR Code Transfer

## Technology Stack

### Backend
- FastAPI 0.104.1
- Python 3.9+
- PostgreSQL 13+
- SQLAlchemy 2.0.23
- Alembic 1.12.1
- Pydantic 2.5.0
- python-jose (JWT)
- passlib (Bcrypt)
- google-auth

### Frontend
- React 18.2.0
- React Router 6.20.0
- Axios 1.6.2
- html5-qrcode 2.3.8
- qrcode 1.5.3
- @react-oauth/google 0.12.1

### Database
- PostgreSQL 13+
- UUID extension
- Timestamp functions
- Foreign keys

### Infrastructure
- Uvicorn (ASGI server)
- Node.js 16+
- npm/yarn
- Git

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Security Compliance

- ✅ HTTPS support (production)
- ✅ Secure cookies (production)
- ✅ CORS configuration
- ✅ SQL injection prevention
- ✅ XSS prevention (React escaping)
- ✅ CSRF protection (JWT tokens)
- ✅ Password hashing (Bcrypt)
- ✅ OAuth 2.0 standard

---

**Built with ❤️ by Gaurang Kothari (X Googler)**


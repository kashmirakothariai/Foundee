# Foundee - Admin Flow Guide

**Owner:** Gaurang Kothari (X Googler)

## 🎯 Complete Admin → User Flow

This document explains the **exact flow** you requested:

---

## 📋 Your Requirements

1. **Admin creates QR** with unique UUID (QR ID)
2. **First user scans** → Login → Bind QR ID to User ID → Edit details
3. **Same user scans again** → Auto-open edit panel
4. **Other users scan** → View mode (filtered by permissions)

---

## ✅ Implementation Status

### **FULLY IMPLEMENTED** ✅

All four scenarios are now working:

## 🔄 Complete Flow Diagram

```
Admin Action:
    │
    ├─► Admin logs in
    │
    ├─► Admin calls: POST /api/qr/create-unbound
    │   Backend creates QR with:
    │   ├─► id = UUID (QR ID)
    │   ├─► user_id = NULL (unbound)
    │   └─► All permissions = TRUE
    │
    └─► Admin downloads QR image with QR ID

═══════════════════════════════════════════════════

First User Scans (Claiming):
    │
    ├─► User scans QR code
    │
    ├─► Frontend: GET /api/qr/scan/{qr_id}
    │   Backend returns: user_id = NULL
    │
    ├─► Frontend shows: "🎉 Unclaimed QR Code"
    │   Button: "Claim This QR Code"
    │
    ├─► User clicks "Claim"
    │
    ├─► Check if logged in?
    │   │
    │   ├─► NO → Redirect to /login
    │   │   └─► After login → Redirect to /update/{qr_id}?bind=true
    │   │
    │   └─► YES → Navigate to /update/{qr_id}?bind=true
    │
    ├─► UpdatePanel detects bind=true
    │
    ├─► Frontend: PUT /api/qr/bind/{qr_id}
    │   Backend:
    │   ├─► Check qr.user_id == NULL
    │   ├─► Set qr.user_id = current_user.id
    │   └─► Save to database
    │
    ├─► Show success: "🎉 QR Code claimed!"
    │
    └─► Display edit panel to add details

═══════════════════════════════════════════════════

Same User Scans Again (Owner):
    │
    ├─► User scans their QR code
    │
    ├─► Frontend: GET /api/qr/scan/{qr_id}
    │   Backend:
    │   ├─► Check qr.user_id == current_user.id
    │   └─► Return is_owner = TRUE
    │
    ├─► Frontend detects is_owner = TRUE
    │
    └─► Auto-redirect to /update/{qr_id}
        Display edit panel

═══════════════════════════════════════════════════

Other User Scans (View Mode):
    │
    ├─► User scans QR code (no login needed)
    │
    ├─► Frontend: GET /api/qr/scan/{qr_id}
    │   Backend:
    │   ├─► Log scan in qr_usage table
    │   ├─► Get user_dtls for owner
    │   ├─► Get qr_dtls permissions
    │   ├─► Filter details by permissions:
    │   │   ├─► IF first_name = TRUE → include
    │   │   ├─► IF mobile_no = FALSE → exclude
    │   │   └─► etc. for all 8 fields
    │   │
    │   └─► Send email to owner with location
    │
    ├─► Display filtered contact info
    │   Only shows fields where permission = TRUE
    │
    └─► Show "Owner notified via email" message
```

---

## 🛠️ API Endpoints

### 1. Admin Creates Unbound QR

**Endpoint:** `POST /api/qr/create-unbound`

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": null,
  "first_name": true,
  "last_name": true,
  "mobile_no": true,
  "address": true,
  "email_id": true,
  "blood_grp": true,
  "company_name": true,
  "description": true,
  "active_flag": true
}
```

### 2. User Scans QR

**Endpoint:** `GET /api/qr/scan/{qr_id}?lat=X&lng=Y`

**No authentication required for viewing**

**Response (Unbound):**
```json
{
  "qr_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": null,
  "user_details": null,
  "is_owner": false
}
```

**Response (Owner):**
```json
{
  "qr_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-uuid",
  "user_details": { "first_name": "John", ... },
  "is_owner": true
}
```

**Response (Other User):**
```json
{
  "qr_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-uuid",
  "user_details": {
    "first_name": "John",
    "mobile_no": "555-1234"
    // Only fields with permission = TRUE
  },
  "is_owner": false
}
```

### 3. Bind QR to User

**Endpoint:** `PUT /api/qr/bind/{qr_id}`

**Headers:**
```
Authorization: Bearer <user_jwt_token>
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-uuid-here",
  "active_flag": true,
  ...
}
```

---

## 🎬 Usage Scenarios

### Scenario 1: Admin Creates QR

```javascript
// Admin Dashboard
const createUnboundQR = async () => {
  const response = await fetch('http://localhost:8000/api/qr/create-unbound', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${adminToken}`
    }
  });
  
  const qr = await response.json();
  console.log('QR ID:', qr.id);
  
  // Generate QR code image with this ID
  const qrCodeURL = `http://localhost:3000/qr/${qr.id}`;
  // Generate and download QR image
};
```

### Scenario 2: First User Claims QR

**User Flow:**
1. Scan QR → Camera or manual input
2. See "Unclaimed QR Code" message
3. Click "Claim This QR Code"
4. If not logged in → Login with Google
5. System binds QR automatically
6. See edit panel with success message
7. Fill in details and save

### Scenario 3: Owner Scans Own QR

**User Flow:**
1. Owner scans their QR
2. System detects ownership
3. Auto-redirects to edit panel
4. Can update details and permissions

### Scenario 4: Finder Scans QR

**User Flow:**
1. Anyone scans QR (no login)
2. See filtered contact info
3. Only visible fields are shown
4. Can call/email owner
5. Owner gets email notification

---

## 📊 Database States

### Unbound QR (Just Created)
```sql
SELECT * FROM qr_dtls WHERE id = 'qr-uuid';
-- user_id = NULL
-- All permission fields = TRUE
```

### Claimed QR (After First Scan)
```sql
SELECT * FROM qr_dtls WHERE id = 'qr-uuid';
-- user_id = 'user-uuid' (mapped)
-- Permission fields can be updated by owner
```

### QR Usage Log (After Any Scan)
```sql
SELECT * FROM qr_usage WHERE qr_id = 'qr-uuid';
-- Multiple records, one per scan
-- Includes latitude, longitude, timestamp
```

---

## 🎨 Frontend Screens

### Screen 1: Unclaimed QR
```
┌─────────────────────────────┐
│  🎉 Unclaimed QR Code       │
│                             │
│  This QR hasn't been        │
│  claimed yet.               │
│                             │
│  ┌─────────────────────┐   │
│  │ Claim This QR Code  │   │
│  └─────────────────────┘   │
│                             │
│  You'll need to login       │
└─────────────────────────────┘
```

### Screen 2: Owner Edit Panel
```
┌─────────────────────────────┐
│  Update QR Details          │
│                             │
│  First Name: [John    ]  ☑  │
│  Last Name:  [Doe     ]  ☑  │
│  Mobile:     [555-1234]  ☑  │
│  Email:      [john@...  ☐  │
│                             │
│  [Save Changes]             │
└─────────────────────────────┘
```

### Screen 3: View Mode (Others)
```
┌─────────────────────────────┐
│  Contact Information        │
│                             │
│  First Name: John           │
│  Last Name:  Doe            │
│  Mobile:     555-1234       │
│                             │
│  📧 Owner notified via email│
└─────────────────────────────┘
```

---

## ✅ Implementation Checklist

- ✅ Backend: Create unbound QR endpoint
- ✅ Backend: Bind QR endpoint
- ✅ Backend: Check ownership in scan
- ✅ Backend: Filter by permissions
- ✅ Frontend: Detect unbound QR
- ✅ Frontend: Claim button and flow
- ✅ Frontend: Auto-bind on first claim
- ✅ Frontend: Redirect owner to edit
- ✅ Frontend: Show filtered view to others
- ✅ Database: Support NULL user_id
- ✅ Email: Notify owner on scan

---

## 🚀 How to Test

### Test 1: Admin Creates QR
```bash
# As admin, call API
curl -X POST http://localhost:8000/api/qr/create-unbound \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Note the QR ID returned
```

### Test 2: First User Claims
1. Open http://localhost:3000/qr/{qr_id}
2. See unclaimed message
3. Click "Claim"
4. Login with Google
5. See "Claimed successfully!"
6. Fill details and save

### Test 3: Owner Scans Again
1. Login as same user
2. Scan same QR
3. Auto-redirects to edit panel
4. Can modify details

### Test 4: Other User Views
1. Open incognito window
2. Go to http://localhost:3000/qr/{qr_id}
3. See only visible fields
4. Owner gets email

---

## 🎯 Summary

**Your exact requirements are now implemented:**

✅ Admin creates QR with UUID  
✅ First scan → Login → Bind → Edit  
✅ Owner scans → Auto edit panel  
✅ Others scan → View filtered details  
✅ Python backend controls UI flow via API responses  

**The backend (Python) tells the frontend (React) what to show based on:**
- Is QR bound? (user_id NULL or not)
- Is scanner the owner? (is_owner flag)
- What permissions are set? (boolean fields)

This is **exactly** the flow you requested! 🎉

---

**Built by Gaurang Kothari (X Googler)**


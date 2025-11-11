# 📝 Logging Guide - Foundee Application

**Owner:** Gaurang Kothari (X Googler)

---

## 🎯 Overview

The Foundee application now has comprehensive logging with proper exception handling to track application flow and debug issues efficiently.

## 📂 Log Files Location

All logs are stored in: `backend/logs/`

### Log Files Generated:

1. **`foundee_YYYY-MM-DD.log`** - Main application logs (INFO, WARNING, ERROR)
2. **`foundee_errors_YYYY-MM-DD.log`** - Error logs only (ERROR level)

### Log Rotation:
- **Max file size:** 10MB per file
- **Backup count:** 5 files
- Files automatically rotate when size limit is reached

---

## 📊 Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| **INFO** | Normal flow tracking | User login, QR scan, email sent |
| **WARNING** | Unexpected but handled situations | Invalid credentials, missing data |
| **ERROR** | Errors with full traceback | Database errors, email failures |
| **DEBUG** | Detailed debug information | Currently minimal usage |

---

## 🔍 Logger Modules

The application has separate loggers for different modules:

### 1. **Authentication Logger** (`foundee.auth`)
- Tracks Google OAuth login flow
- Tracks email/password login
- Logs user creation and token generation

### 2. **QR Logger** (`foundee.qr`)
- Tracks QR code creation
- Tracks QR code scanning (most detailed)
- Logs permission updates and binding

### 3. **User Logger** (`foundee.user`)
- Tracks user detail retrieval
- Tracks user detail updates

### 4. **Email Logger** (`foundee.email`)
- Tracks email sending process
- Logs SMTP connection details
- Logs email delivery success/failure

### 5. **Main Logger** (`foundee.main`)
- Tracks application startup/shutdown
- Logs all HTTP requests and responses
- Tracks request duration

---

## 🔎 Flow Tracking Examples

### Google Login Flow:
```
2024-01-15 10:30:45 - foundee.auth - INFO - === Google Login Flow Started ===
2024-01-15 10:30:45 - foundee.auth - INFO - Verifying Google OAuth token
2024-01-15 10:30:46 - foundee.auth - INFO - Google token verified successfully for email: user@example.com
2024-01-15 10:30:46 - foundee.auth - INFO - Checking if user exists in database: user@example.com
2024-01-15 10:30:46 - foundee.auth - INFO - Creating new user account for: user@example.com
2024-01-15 10:30:46 - foundee.auth - INFO - User account created successfully with ID: 123
2024-01-15 10:30:46 - foundee.auth - INFO - Creating JWT access token for user: user@example.com
2024-01-15 10:30:46 - foundee.auth - INFO - Google login successful for user: user@example.com
2024-01-15 10:30:46 - foundee.auth - INFO - === Google Login Flow Completed ===
```

### QR Scan Flow:
```
2024-01-15 10:35:20 - foundee.qr - INFO - === QR Scan Flow Started ===
2024-01-15 10:35:20 - foundee.qr - INFO - Scanning QR ID: abc123-def456-ghi789
2024-01-15 10:35:20 - foundee.qr - INFO - Scanner: finder@example.com
2024-01-15 10:35:20 - foundee.qr - INFO - Location: Lat=40.7128, Long=-74.0060
2024-01-15 10:35:20 - foundee.qr - INFO - QR found - User ID: 123
2024-01-15 10:35:20 - foundee.qr - INFO - QR usage logged successfully
2024-01-15 10:35:20 - foundee.qr - INFO - Is owner: False
2024-01-15 10:35:20 - foundee.qr - INFO - Sending location alert email to owner: owner@example.com
2024-01-15 10:35:21 - foundee.email - INFO - Email sent successfully to: owner@example.com
2024-01-15 10:35:21 - foundee.qr - INFO - Filtering user details based on QR permissions
2024-01-15 10:35:21 - foundee.qr - INFO - Filtered details count: 5 fields
2024-01-15 10:35:21 - foundee.qr - INFO - === QR Scan Flow Completed ===
```

### HTTP Request Flow:
```
2024-01-15 10:35:20 - foundee.main - INFO - >>> Incoming Request: GET /api/qr/scan/abc123-def456
2024-01-15 10:35:20 - foundee.main - INFO - >>> Client: 192.168.1.100
2024-01-15 10:35:21 - foundee.main - INFO - <<< Response: 200 | Duration: 0.523s
```

---

## ❌ Error Tracking

All errors are logged with full stack traces for debugging:

### Example Error Log:
```
2024-01-15 10:40:15 - foundee.qr - ERROR - Database error while creating QR: connection timeout
Traceback (most recent call last):
  File "app/routes/qr.py", line 58, in create_qr
    db.commit()
  ...
SQLAlchemyError: connection timeout
```

### Error Categories Tracked:

1. **Authentication Errors:**
   - Invalid Google tokens
   - Invalid credentials
   - User creation failures

2. **Database Errors:**
   - Connection failures
   - Query errors
   - Transaction rollbacks

3. **Email Errors:**
   - SMTP authentication failures
   - Connection errors
   - Send failures

4. **General Errors:**
   - Unexpected exceptions
   - Validation errors

---

## 🛠️ Using Logs for Debugging

### 1. Find User Login Issues:
```bash
grep "Login Flow" backend/logs/foundee_*.log
```

### 2. Track Specific QR Scan:
```bash
grep "QR ID: abc123" backend/logs/foundee_*.log
```

### 3. Find All Errors:
```bash
cat backend/logs/foundee_errors_*.log
```

### 4. Track Email Delivery:
```bash
grep "Email sent" backend/logs/foundee_*.log
```

### 5. Monitor API Performance:
```bash
grep "Duration:" backend/logs/foundee_*.log
```

---

## 📈 Log Format

```
TIMESTAMP - LOGGER_NAME - LEVEL - [FILE:LINE] - MESSAGE
```

**Example:**
```
2024-01-15 10:30:45 - foundee.auth - INFO - [auth.py:27] - === Google Login Flow Started ===
```

---

## 🔧 Configuration

Logging is configured in `backend/app/logger.py`:

```python
from app.logger import auth_logger, qr_logger, user_logger, email_logger

# Use in your code:
auth_logger.info("Message")
auth_logger.error("Error message", exc_info=True)  # Include stack trace
```

---

## 📝 Best Practices

### ✅ DO:
- Use `logger.info()` for flow tracking
- Use `logger.warning()` for handled issues
- Use `logger.error()` with `exc_info=True` for exceptions
- Log entry and exit of important flows
- Log important business events (QR scan, user creation)

### ❌ DON'T:
- Log sensitive data (passwords, tokens)
- Log in tight loops (performance impact)
- Use `print()` statements (use logger instead)

---

## 🚀 Quick Reference

### Import Loggers:
```python
from app.logger import auth_logger, qr_logger, user_logger, email_logger
```

### Log Flow Start/End:
```python
logger.info("=== Flow Name Started ===")
# ... code ...
logger.info("=== Flow Name Completed ===")
```

### Log with Exception:
```python
try:
    # code
except Exception as e:
    logger.error(f"Error message: {str(e)}", exc_info=True)
    raise
```

---

## 📊 Monitoring Tips

1. **Check logs daily** for errors in `foundee_errors_*.log`
2. **Monitor email delivery** for location alerts
3. **Track login patterns** for security
4. **Analyze request duration** for performance optimization
5. **Review QR scan logs** for usage patterns

---

## 🔍 Troubleshooting

### If logs are not appearing:

1. **Check logs directory exists:**
   ```bash
   ls backend/logs/
   ```

2. **Check file permissions:**
   ```bash
   # On Unix/Linux:
   chmod 755 backend/logs
   ```

3. **Check logger initialization:**
   - Logs are created automatically on first import
   - Check `backend/app/logger.py` is imported

### If logs are too verbose:

Adjust log level in `backend/app/logger.py`:
```python
logger.setLevel(logging.WARNING)  # Only WARNING and ERROR
```

---

## 📞 Support

For logging issues or questions:
- Check this guide first
- Review log files in `backend/logs/`
- Contact: Gaurang Kothari (X Googler)

---

**Last Updated:** 2024
**Version:** 1.0.0


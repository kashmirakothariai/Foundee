from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, qr, user
import logging
import time

# Set up main application logger
app_logger = logging.getLogger("foundee.main")
app_logger.setLevel(logging.INFO)

app = FastAPI(
    title="Foundee API",
    description="QR-based Lost and Found Application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    app_logger.info(f">>> Incoming Request: {request.method} {request.url.path}")
    app_logger.info(f">>> Client: {request.client.host if request.client else 'Unknown'}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate request duration
    duration = time.time() - start_time
    
    # Log response
    app_logger.info(f"<<< Response: {response.status_code} | Duration: {duration:.3f}s")
    
    return response

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(qr.router, prefix="/api")
app.include_router(user.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    app_logger.info("=" * 80)
    app_logger.info("🚀 Foundee API Starting Up")
    app_logger.info(f"📌 Version: 1.0.0")
    app_logger.info(f"📌 Environment: {settings.FRONTEND_URL}")
    app_logger.info(f"📌 Owner: Gaurang Kothari (X Googler)")
    app_logger.info("=" * 80)

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("=" * 80)
    app_logger.info("🛑 Foundee API Shutting Down")
    app_logger.info("=" * 80)

@app.get("/")
def root():
    app_logger.info("Root endpoint accessed")
    return {
        "message": "Foundee API",
        "owner": "Gaurang Kothari (X Googler)",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    app_logger.debug("Health check endpoint accessed")
    return {"status": "healthy"}


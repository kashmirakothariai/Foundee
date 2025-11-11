from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import timedelta
from app.database import get_db
from app.models import UserLogin, UserDetails
from app.schemas import Token, UserLoginResponse
from app.auth import create_access_token, get_password_hash, verify_password
from app.config import settings
from app.logger import auth_logger
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class GoogleLoginRequest(BaseModel):
    token: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/google-login", response_model=Token)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Login or register user with Google OAuth"""
    auth_logger.info("=== Google Login Flow Started ===")
    
    try:
        # Verify Google token
        auth_logger.info("Verifying Google OAuth token")
        idinfo = id_token.verify_oauth2_token(
            request.token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        
        email = idinfo.get('email')
        name = idinfo.get('name', email.split('@')[0] if email else 'Unknown')
        auth_logger.info(f"Google token verified successfully for email: {email}")
        
        if not email:
            auth_logger.error("Email not found in Google account")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not found in Google account"
            )
        
        # Check if user exists
        auth_logger.info(f"Checking if user exists in database: {email}")
        user = db.query(UserLogin).filter(UserLogin.email_id == email).first()
        
        if not user:
            # Create new user
            auth_logger.info(f"Creating new user account for: {email}")
            try:
                user = UserLogin(
                    name=name,
                    email_id=email,
                    password=None,  # No password for OAuth users
                    active_flag=True
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                auth_logger.info(f"User account created successfully with ID: {user.id}")
                
                # Create empty user details
                auth_logger.info(f"Creating user details for user ID: {user.id}")
                user_details = UserDetails(
                    user_id=user.id,
                    email_id=email,
                    crt_by=user.id
                )
                db.add(user_details)
                db.commit()
                auth_logger.info("User details created successfully")
                
            except SQLAlchemyError as e:
                auth_logger.error(f"Database error while creating user: {str(e)}", exc_info=True)
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user account"
                )
        else:
            auth_logger.info(f"Existing user found with ID: {user.id}")
        
        # Create access token
        auth_logger.info(f"Creating JWT access token for user: {email}")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email_id, "user_id": str(user.id)},
            expires_delta=access_token_expires
        )
        
        auth_logger.info(f"Google login successful for user: {email}")
        auth_logger.info("=== Google Login Flow Completed ===")
        return {"access_token": access_token, "token_type": "bearer"}
    
    except ValueError as e:
        auth_logger.error(f"Invalid Google token: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    except HTTPException:
        raise
    except Exception as e:
        auth_logger.error(f"Unexpected error during Google login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with email and password (optional, for non-OAuth users)"""
    auth_logger.info("=== Email/Password Login Flow Started ===")
    auth_logger.info(f"Login attempt for email: {request.email}")
    
    try:
        user = db.query(UserLogin).filter(UserLogin.email_id == request.email).first()
        
        if not user:
            auth_logger.warning(f"Login failed: User not found for email: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.password:
            auth_logger.warning(f"Login failed: No password set for OAuth user: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not verify_password(request.password, user.password):
            auth_logger.warning(f"Login failed: Invalid password for user: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        auth_logger.info(f"Password verified successfully for user: {request.email}")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email_id, "user_id": str(user.id)},
            expires_delta=access_token_expires
        )
        
        auth_logger.info(f"Login successful for user: {request.email}")
        auth_logger.info("=== Email/Password Login Flow Completed ===")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        auth_logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )


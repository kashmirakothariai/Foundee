from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.database import get_db
from app.models import UserLogin, UserDetails
from app.schemas import UserDetailsUpdate, UserDetailsResponse, UserLoginResponse
from app.auth import require_auth
from app.logger import user_logger

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=UserLoginResponse)
def get_current_user_info(current_user: UserLogin = Depends(require_auth)):
    """Get current user information"""
    user_logger.info(f"User info requested for: {current_user.email_id} (ID: {current_user.id})")
    return current_user

@router.get("/details", response_model=UserDetailsResponse)
def get_user_details(
    current_user: UserLogin = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get current user's details"""
    user_logger.info(f"=== Get User Details Flow Started ===")
    user_logger.info(f"Fetching details for user: {current_user.email_id} (ID: {current_user.id})")
    
    try:
        # Since it's now one-to-many, get the first (primary) user details record
        user_details = db.query(UserDetails).filter(UserDetails.user_id == current_user.id).first()
        
        if not user_details:
            user_logger.warning(f"User details not found for user ID: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User details not found"
            )
        
        user_logger.info("User details retrieved successfully")
        user_logger.info("=== Get User Details Flow Completed ===")
        return user_details
        
    except HTTPException:
        raise
    except Exception as e:
        user_logger.error(f"Unexpected error while fetching user details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.put("/details", response_model=UserDetailsResponse)
def update_user_details(
    details_update: UserDetailsUpdate,
    current_user: UserLogin = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Update current user's details"""
    user_logger.info("=== Update User Details Flow Started ===")
    user_logger.info(f"User {current_user.email_id} (ID: {current_user.id}) updating details")
    
    try:
        user_details = db.query(UserDetails).filter(UserDetails.user_id == current_user.id).first()
        
        if not user_details:
            user_logger.warning(f"User details not found for user ID: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User details not found"
            )
        
        # Update fields
        update_data = details_update.model_dump(exclude_unset=True)
        user_logger.info(f"Updating fields: {list(update_data.keys())}")
        
        for field, value in update_data.items():
            setattr(user_details, field, value)
        
        user_details.lst_updt_by = current_user.id
        
        db.commit()
        db.refresh(user_details)
        
        user_logger.info("User details updated successfully")
        user_logger.info("=== Update User Details Flow Completed ===")
        return user_details
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        user_logger.error(f"Database error while updating user details: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user details"
        )
    except Exception as e:
        user_logger.error(f"Unexpected error while updating user details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.models import UserLogin, UserDetails, QRDetails, QRUsage
from app.schemas import (
    QRDetailsCreate, QRDetailsResponse, QRDetailsUpdate,
    QRUsageCreate, QRUsageResponse, QRScanResponse,
    UserDetailsUpdate, UserDetailsResponse
)
from app.auth import get_current_user, require_auth, require_admin
from app.email_service import email_service
from app.logger import qr_logger

router = APIRouter(prefix="/qr", tags=["QR Code"])

@router.post("/create", response_model=QRDetailsResponse)
def create_qr(
    qr_data: QRDetailsCreate,
    current_user: UserLogin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new QR code (requires authentication)"""
    qr_logger.info("=== Create QR Flow Started ===")
    qr_logger.info(f"User {current_user.email_id} (ID: {current_user.id}) creating new QR")
    
    try:
        # If user_dtls_id not provided, get the user's details ID
        if not qr_data.user_dtls_id:
            # Get the user's details record
            user_details = db.query(UserDetails).filter(UserDetails.user_id == current_user.id).first()
            if not user_details:
                qr_logger.error(f"No user details found for user: {current_user.id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User details not found. Please update your profile first."
                )
            qr_data.user_dtls_id = user_details.id
            qr_logger.info(f"No user_dtls_id provided, using current user's details: {user_details.id}")
        
        # Verify user owns this user_details record
        user_details = db.query(UserDetails).filter(UserDetails.id == qr_data.user_dtls_id).first()
        if not user_details or user_details.user_id != current_user.id:
            qr_logger.warning(f"User {current_user.id} attempted to create QR for another user's details: {qr_data.user_dtls_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create QR for another user's details"
            )
        
        qr_logger.info(f"Creating QR with permissions - FirstName: {qr_data.first_name}, LastName: {qr_data.last_name}, Mobile: {qr_data.mobile_no}")
        
        qr = QRDetails(
            user_dtls_id=qr_data.user_dtls_id,
            first_name=qr_data.first_name,
            last_name=qr_data.last_name,
            mobile_no=qr_data.mobile_no,
            address=qr_data.address,
            email_id=qr_data.email_id,
            blood_grp=qr_data.blood_grp,
            company_name=qr_data.company_name,
            description=qr_data.description,
            crt_by=current_user.id
        )
        
        db.add(qr)
        db.commit()
        db.refresh(qr)
        
        qr_logger.info(f"QR created successfully with ID: {qr.id}")
        qr_logger.info("=== Create QR Flow Completed ===")
        return qr
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        qr_logger.error(f"Database error while creating QR: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create QR code"
        )
    except Exception as e:
        qr_logger.error(f"Unexpected error while creating QR: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/create-unbound", response_model=QRDetailsResponse)
def create_unbound_qr(
    current_user: UserLogin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Create an UNBOUND QR code (Admin/ASP Admin only)
    QR is created with user_id = NULL
    First user to scan and login will claim this QR
    """
    # Create unbound QR with NULL user_dtls_id
    qr = QRDetails(
        user_dtls_id=None,  # UNBOUND - no owner yet
        first_name=True,
        last_name=True,
        mobile_no=True,
        address=True,
        email_id=True,
        blood_grp=True,
        company_name=True,
        description=True,
        crt_by=current_user.id  # Track who created it (admin)
    )
    
    db.add(qr)
    db.commit()
    db.refresh(qr)
    
    return qr

@router.get("/scan/{qr_id}", response_model=QRScanResponse)
def scan_qr(
    qr_id: UUID,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    current_user: Optional[UserLogin] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Scan QR code - public endpoint (no auth required for viewing)
    If current_user is provided, checks if they're the owner
    """
    qr_logger.info("=== QR Scan Flow Started ===")
    qr_logger.info(f"Scanning QR ID: {qr_id}")
    qr_logger.info(f"Scanner: {current_user.email_id if current_user else 'Anonymous'}")
    qr_logger.info(f"Location: Lat={latitude}, Long={longitude}")
    
    try:
        qr = db.query(QRDetails).filter(QRDetails.id == qr_id, QRDetails.active_flag == True).first()
        
        if not qr:
            qr_logger.warning(f"QR Code not found or inactive: {qr_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR Code not found"
            )
        
        qr_logger.info(f"QR found - User Details ID: {qr.user_dtls_id if qr.user_dtls_id else 'Unbound'}")
        
        # Log QR usage
        try:
            qr_usage = QRUsage(
                qr_id=qr_id,
                latitude=latitude,
                longitude=longitude,
                crt_by=current_user.id if current_user else None
            )
            db.add(qr_usage)
            db.commit()
            qr_logger.info("QR usage logged successfully")
        except SQLAlchemyError as e:
            qr_logger.error(f"Failed to log QR usage: {str(e)}", exc_info=True)
            db.rollback()
            # Continue despite logging failure
        
        # Check if scanner is the owner
        is_owner = False
        if current_user and qr.user_dtls_id:
            # Check if current user owns the user_details record
            user_details_check = db.query(UserDetails).filter(
                UserDetails.id == qr.user_dtls_id,
                UserDetails.user_id == current_user.id
            ).first()
            is_owner = user_details_check is not None
        qr_logger.info(f"Is owner: {is_owner}")
        
        # If not bound to user details yet
        if not qr.user_dtls_id:
            qr_logger.info("QR is unbound (no user details assigned)")
            qr_logger.info("=== QR Scan Flow Completed ===")
            return QRScanResponse(
                qr_id=qr.id,
                user_dtls_id=None,
                user_details=None,
                is_owner=False
            )
        
        # Get user details
        user_details = db.query(UserDetails).filter(UserDetails.id == qr.user_dtls_id).first()
        
        # Get owner's login info for email
        owner = None
        if user_details:
            owner = db.query(UserLogin).filter(UserLogin.id == user_details.user_id).first()
        
        # Send email notification to owner (only if not scanning own QR)
        if owner and not is_owner:
            qr_logger.info(f"Sending location alert email to owner: {owner.email_id}")
            try:
                email_service.send_location_alert(
                    to_email=owner.email_id,
                    qr_id=str(qr_id),
                    latitude=latitude,
                    longitude=longitude
                )
                qr_logger.info("Location alert email sent successfully")
            except Exception as e:
                qr_logger.error(f"Failed to send location alert email: {str(e)}", exc_info=True)
                # Continue despite email failure
        else:
            qr_logger.info("No email sent - owner scanning own QR or owner not found")
        
        # Filter user details based on QR permissions
        filtered_details = {}
        if user_details:
            qr_logger.info("Filtering user details based on QR permissions")
            if qr.first_name:
                filtered_details['first_name'] = user_details.first_name
            if qr.last_name:
                filtered_details['last_name'] = user_details.last_name
            if qr.mobile_no:
                filtered_details['mobile_no'] = user_details.mobile_no
            if qr.address:
                filtered_details['address'] = user_details.address
            if qr.email_id:
                filtered_details['email_id'] = user_details.email_id
            if qr.blood_grp:
                filtered_details['blood_grp'] = user_details.blood_grp
            if qr.company_name:
                filtered_details['company_name'] = user_details.company_name
            if qr.description:
                filtered_details['description'] = user_details.description
            qr_logger.info(f"Filtered details count: {len(filtered_details)} fields")
        else:
            qr_logger.warning(f"No user details found for user_dtls_id: {qr.user_dtls_id}")
        
        qr_logger.info("=== QR Scan Flow Completed ===")
        return QRScanResponse(
            qr_id=qr.id,
            user_dtls_id=qr.user_dtls_id,
            user_details=filtered_details if filtered_details else None,
            is_owner=is_owner
        )
        
    except HTTPException:
        raise
    except Exception as e:
        qr_logger.error(f"Unexpected error during QR scan: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while scanning QR"
        )

@router.get("/details/{qr_id}", response_model=QRDetailsResponse)
def get_qr_details(
    qr_id: UUID,
    current_user: UserLogin = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get QR details including permissions (requires authentication and ownership)"""
    qr = db.query(QRDetails).filter(QRDetails.id == qr_id).first()
    
    if not qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code not found"
        )
    
    # Only owner can view full QR details with permissions
    if qr.user_dtls_id:
        user_details = db.query(UserDetails).filter(UserDetails.id == qr.user_dtls_id).first()
        if not user_details or user_details.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view QR details"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="QR code is not bound to any user"
        )
    
    return qr

@router.put("/update-permissions/{qr_id}", response_model=QRDetailsResponse)
def update_qr_permissions(
    qr_id: UUID,
    qr_update: QRDetailsUpdate,
    current_user: UserLogin = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Update QR code visibility permissions (owner only)"""
    qr = db.query(QRDetails).filter(QRDetails.id == qr_id).first()
    
    if not qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code not found"
        )
    
    if qr.user_dtls_id:
        user_details = db.query(UserDetails).filter(UserDetails.id == qr.user_dtls_id).first()
        if not user_details or user_details.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this QR"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="QR code is not bound to any user"
        )
    
    # Update permissions
    qr.first_name = qr_update.first_name
    qr.last_name = qr_update.last_name
    qr.mobile_no = qr_update.mobile_no
    qr.address = qr_update.address
    qr.email_id = qr_update.email_id
    qr.blood_grp = qr_update.blood_grp
    qr.company_name = qr_update.company_name
    qr.description = qr_update.description
    qr.lst_updt_by = current_user.id
    
    db.commit()
    db.refresh(qr)
    
    return qr

@router.put("/bind/{qr_id}", response_model=QRDetailsResponse)
def bind_qr_to_user(
    qr_id: UUID,
    current_user: UserLogin = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Bind an unbound QR code to the current user (First scan claim)
    This is called when a user scans an unbound QR and logs in
    """
    qr = db.query(QRDetails).filter(QRDetails.id == qr_id).first()
    
    if not qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code not found"
        )
    
    if qr.user_dtls_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="QR Code is already bound to a user"
        )
    
    # Get current user's details
    user_details = db.query(UserDetails).filter(UserDetails.user_id == current_user.id).first()
    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User details not found. Please update your profile first."
        )
    
    # Bind QR to current user's details
    qr.user_dtls_id = user_details.id
    qr.lst_updt_by = current_user.id
    
    db.commit()
    db.refresh(qr)
    
    return qr

@router.get("/my-qr-codes", response_model=list[QRDetailsResponse])
def get_my_qr_codes(
    current_user: UserLogin = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get all QR codes belonging to current user"""
    # Get all user_details records for current user
    user_details_list = db.query(UserDetails).filter(UserDetails.user_id == current_user.id).all()
    user_details_ids = [ud.id for ud in user_details_list]
    
    if not user_details_ids:
        return []
    
    qr_codes = db.query(QRDetails).filter(
        QRDetails.user_dtls_id.in_(user_details_ids),
        QRDetails.active_flag == True
    ).all()
    
    return qr_codes


from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# User Login Schemas
class UserLoginBase(BaseModel):
    name: str
    email_id: EmailStr

class UserLoginCreate(UserLoginBase):
    password: Optional[str] = None

class UserLoginResponse(UserLoginBase):
    id: UUID
    active_flag: bool
    crt_dt: datetime
    
    class Config:
        from_attributes = True

# User Details Schemas
class UserDetailsBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_no: Optional[str] = None
    address: Optional[str] = None
    email_id: Optional[str] = None
    blood_grp: Optional[str] = None
    company_name: Optional[str] = None
    description: Optional[str] = None

class UserDetailsCreate(UserDetailsBase):
    user_id: UUID

class UserDetailsUpdate(UserDetailsBase):
    pass

class UserDetailsResponse(UserDetailsBase):
    id: UUID
    user_id: UUID
    active_flag: bool
    
    class Config:
        from_attributes = True

# QR Details Schemas
class QRDetailsBase(BaseModel):
    first_name: bool = True
    last_name: bool = True
    mobile_no: bool = True
    address: bool = True
    email_id: bool = True
    blood_grp: bool = True
    company_name: bool = True
    description: bool = True

class QRDetailsCreate(QRDetailsBase):
    user_dtls_id: Optional[UUID] = None

class QRDetailsUpdate(QRDetailsBase):
    pass

class QRDetailsResponse(QRDetailsBase):
    id: UUID
    user_dtls_id: Optional[UUID]
    active_flag: bool
    
    class Config:
        from_attributes = True

# QR Usage Schemas
class QRUsageCreate(BaseModel):
    qr_id: UUID
    latitude: Optional[str] = None
    longitude: Optional[str] = None

class QRUsageResponse(BaseModel):
    id: UUID
    qr_id: UUID
    latitude: Optional[str]
    longitude: Optional[str]
    crt_dt: datetime
    
    class Config:
        from_attributes = True

# QR Scan Response (for viewing)
class QRScanResponse(BaseModel):
    qr_id: UUID
    user_dtls_id: Optional[UUID]
    user_details: Optional[dict] = None  # Filtered based on permissions
    is_owner: bool = False

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID] = None


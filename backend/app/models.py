from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class UserLogin(Base):
    __tablename__ = "user_login"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    email_id = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=True)  # Optional for OAuth users
    role = Column(Integer, default=1, nullable=False)  # 1=user, 2=admin, 3=aspadmin
    active_flag = Column(Boolean, default=True, nullable=False)
    crt_dt = Column(DateTime, default=datetime.utcnow, nullable=False)
    crt_by = Column(UUID(as_uuid=True), nullable=True)
    lst_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lst_updt_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Relationships - Changed to one-to-many for user_details
    user_details = relationship("UserDetails", back_populates="user")

class UserDetails(Base):
    __tablename__ = "user_dtls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_login.id"), nullable=False)  # Removed unique=True for one-to-many
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    mobile_no = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    email_id = Column(String(100), nullable=True)
    blood_grp = Column(String(10), nullable=True)
    company_name = Column(String(200), nullable=True)
    description = Column(String(1000), nullable=True)
    active_flag = Column(Boolean, default=True, nullable=False)
    crt_dt = Column(DateTime, default=datetime.utcnow, nullable=False)
    crt_by = Column(UUID(as_uuid=True), nullable=True)
    lst_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lst_updt_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Relationships
    user = relationship("UserLogin", back_populates="user_details")
    qr_details = relationship("QRDetails", back_populates="user_detail")

class QRDetails(Base):
    __tablename__ = "qr_dtls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_dtls_id = Column(UUID(as_uuid=True), ForeignKey("user_dtls.id"), nullable=True)  # Changed to reference user_dtls.id
    first_name = Column(Boolean, default=True, nullable=False)
    last_name = Column(Boolean, default=True, nullable=False)
    mobile_no = Column(Boolean, default=True, nullable=False)
    address = Column(Boolean, default=True, nullable=False)
    email_id = Column(Boolean, default=True, nullable=False)
    blood_grp = Column(Boolean, default=True, nullable=False)
    company_name = Column(Boolean, default=True, nullable=False)
    description = Column(Boolean, default=True, nullable=False)
    active_flag = Column(Boolean, default=True, nullable=False)
    crt_dt = Column(DateTime, default=datetime.utcnow, nullable=False)
    crt_by = Column(UUID(as_uuid=True), nullable=True)
    lst_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lst_updt_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Relationships
    user_detail = relationship("UserDetails", back_populates="qr_details")
    qr_usage = relationship("QRUsage", back_populates="qr")

class QRUsage(Base):
    __tablename__ = "qr_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    qr_id = Column(UUID(as_uuid=True), ForeignKey("qr_dtls.id"), nullable=False)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    active_flag = Column(Boolean, default=True, nullable=False)
    crt_dt = Column(DateTime, default=datetime.utcnow, nullable=False)
    crt_by = Column(UUID(as_uuid=True), nullable=True)
    lst_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lst_updt_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Relationships
    qr = relationship("QRDetails", back_populates="qr_usage")


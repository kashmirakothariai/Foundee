from cryptography.fernet import Fernet
from app.config import settings
from typing import Optional

class EncryptionService:
    def __init__(self):
        self.enabled = settings.ENCRYPTION_ENABLED
        if self.enabled and settings.ENCRYPTION_KEY:
            self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        else:
            self.cipher = None
    
    def encrypt(self, data: str) -> str:
        """Encrypt data if encryption is enabled, otherwise return as-is"""
        if not self.enabled or not self.cipher or not data:
            return data
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, data: str) -> str:
        """Decrypt data if encryption is enabled, otherwise return as-is"""
        if not self.enabled or not self.cipher or not data:
            return data
        try:
            return self.cipher.decrypt(data.encode()).decode()
        except Exception:
            return data  # Return as-is if decryption fails

encryption_service = EncryptionService()


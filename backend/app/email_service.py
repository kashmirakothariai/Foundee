import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.logger import email_logger
from typing import Optional

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
        email_logger.info("Email service initialized")
    
    def send_location_alert(
        self,
        to_email: str,
        qr_id: str,
        latitude: Optional[str],
        longitude: Optional[str]
    ):
        """Send location alert email to QR owner"""
        email_logger.info("=== Send Location Alert Email Flow Started ===")
        email_logger.info(f"Sending email to: {to_email}")
        email_logger.info(f"QR ID: {qr_id}, Lat: {latitude}, Long: {longitude}")
        
        subject = "Foundee Alert: Your QR Code was Scanned"
        
        location_text = "Location not available"
        if latitude and longitude:
            location_text = f"Latitude: {latitude}, Longitude: {longitude}"
            location_text += f"\nGoogle Maps: https://www.google.com/maps?q={latitude},{longitude}"
            email_logger.info("Location data included in email")
        else:
            email_logger.info("No location data available")
        
        body = f"""
        Hello,
        
        Your Foundee QR Code (ID: {qr_id}) was just scanned!
        
        {location_text}
        
        Time: {self._get_current_time()}
        
        If this was you, you can safely ignore this email.
        
        Best regards,
        Foundee Team
        """
        
        try:
            email_logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                email_logger.info("SMTP connection established, starting TLS")
                server.starttls()
                
                email_logger.info(f"Logging in with user: {self.smtp_user}")
                server.login(self.smtp_user, self.smtp_password)
                
                email_logger.info("Sending email message")
                server.send_message(msg)
            
            email_logger.info(f"Email sent successfully to: {to_email}")
            email_logger.info("=== Send Location Alert Email Flow Completed ===")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            email_logger.error(f"SMTP authentication failed: {str(e)}", exc_info=True)
            return False
        except smtplib.SMTPException as e:
            email_logger.error(f"SMTP error occurred: {str(e)}", exc_info=True)
            return False
        except Exception as e:
            email_logger.error(f"Failed to send email: {str(e)}", exc_info=True)
            return False
    
    def _get_current_time(self):
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

email_service = EmailService()


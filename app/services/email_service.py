import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailService:
    """
    Service class for handling email operations
    """
    
    @staticmethod
    async def send_reset_code(email: str, code: str):
        """
        Send password reset code via email
        For now, just print to console (can be enhanced with real SMTP later)
        """
        print(f"🔐 Password Reset Code for {email}: {code}")
        print(f"📧 Email would be sent to: {email}")
        print(f"💌 Subject: Your MediWay Password Reset Code")
        print(f"📝 Message: Your password reset code is: {code}. This code expires in 15 minutes.")
        
        # TODO: Implement real email sending when needed
        # smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        # smtp_port = int(os.getenv("SMTP_PORT", "587"))
        # smtp_username = os.getenv("SMTP_USERNAME")
        # smtp_password = os.getenv("SMTP_PASSWORD")
        
        return True 
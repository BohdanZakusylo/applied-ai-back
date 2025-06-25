import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional


class EmailService:
    """
    Service class for handling email operations
    """
    
    @staticmethod
    async def send_reset_code(email: str, code: str):
        """
        Send password reset code via email
        """
        # Email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username)
        from_name = os.getenv("SMTP_FROM_NAME", "MediWay Support")
        
        # Check if SMTP is configured
        if not all([smtp_server, smtp_username, smtp_password]):
            print("⚠️  SMTP not configured - falling back to console logging")
            print(f"🔐 Password Reset Code for {email}: {code}")
            print(f"📧 Email would be sent to: {email}")
            print(f"💌 Subject: Your MediWay Password Reset Code")
            print(f"📝 Message: Your password reset code is: {code}. This code expires in 15 minutes.")
            return True
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Your MediWay Password Reset Code"
            message["From"] = f"{from_name} <{from_email}>"
            message["To"] = email
            
            # Email content
            text_content = f"""
Hello,

You requested a password reset for your MediWay account.

Your reset code is: {code}

This code will expire in 15 minutes.

If you didn't request this reset, please ignore this email.

Best regards,
MediWay Support Team
            """.strip()
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #00B9C1; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .code {{ background-color: #fff; border: 2px solid #00B9C1; padding: 15px; font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; letter-spacing: 3px; }}
        .footer {{ padding: 20px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MediWay Password Reset</h1>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>You requested a password reset for your MediWay account.</p>
            <p>Your reset code is:</p>
            <div class="code">{code}</div>
            <p><strong>This code will expire in 15 minutes.</strong></p>
            <p>If you didn't request this reset, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>MediWay Support Team</p>
            <p>This email was sent automatically. Please do not reply.</p>
        </div>
    </div>
</body>
</html>
            """
            
            # Attach text and HTML versions
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")
            message.attach(text_part)
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Enable security
                server.login(smtp_username, smtp_password)
                server.send_message(message)
            
            print(f"✅ Password reset email sent to {email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print(f"❌ SMTP Authentication failed - check username/password")
            print(f"🔐 Fallback: Password reset code for {email}: {code}")
            return False
            
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {e}")
            print(f"🔐 Fallback: Password reset code for {email}: {code}")
            return False
            
        except Exception as e:
            print(f"❌ Email sending error: {e}")
            print(f"🔐 Fallback: Password reset code for {email}: {code}")
            return False 
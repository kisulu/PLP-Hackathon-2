from flask_mail import Mail, Message
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with the app"""
    mail.init_app(app)

def send_bulk_confirmation_emails(users):
    """
    Send confirmation emails to all users who submitted suggestions
    """
    success_count = 0
    
    try:
        # Use Flask-Mail if configured
        if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
            success_count = send_with_flask_mail(users)
        else:
            # Fallback to mock email sending for demo
            success_count = send_mock_emails(users)
            
    except Exception as e:
        print(f"Error sending bulk emails: {e}")
        # Try mock email as fallback
        success_count = send_mock_emails(users)
    
    return success_count

def send_with_flask_mail(users):
    """Send emails using Flask-Mail"""
    success_count = 0
    
    for user in users:
        try:
            msg = Message(
                subject='Thank you for your suggestion! - AI Study Buddy',
                sender=Config.MAIL_DEFAULT_SENDER,
                recipients=[user.email]
            )
            
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #3B82F6, #8B5CF6); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 14px; }}
                    .btn {{ display: inline-block; background: #3B82F6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🧠 AI Study Buddy</h1>
                        <p>Thank you for your valuable feedback!</p>
                    </div>
                    <div class="content">
                        <h2>Hello {user.username}!</h2>
                        <p>We've received your suggestion and really appreciate your feedback. Your input helps us improve AI Study Buddy for students across Africa.</p>
                        
                        <p><strong>What happens next?</strong></p>
                        <ul>
                            <li>Our team will review your suggestion carefully</li>
                            <li>We'll consider implementing it in future updates</li>
                            <li>You'll be notified of any major feature releases</li>
                        </ul>
                        
                        <p>Keep studying smart with AI Study Buddy! 📚</p>
                        
                        <a href="#" class="btn">Continue Studying</a>
                    </div>
                    <div class="footer">
                        <p>AI Study Buddy - Empowering African Students with AI Technology</p>
                        <p>SDG 4: Quality Education | Vibe Coding 3.0 Hackathon</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            mail.send(msg)
            success_count += 1
            print(f"Email sent successfully to {user.email}")
            
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}")
            continue
    
    return success_count

def send_mock_emails(users):
    """Mock email sending for demo purposes"""
    print("=== MOCK EMAIL SYSTEM ===")
    print("Sending bulk confirmation emails...")
    
    for user in users:
        print(f"""
        📧 EMAIL SENT TO: {user.email}
        👤 RECIPIENT: {user.username}
        📋 SUBJECT: Thank you for your suggestion! - AI Study Buddy
        ✅ STATUS: Delivered
        """)
    
    print(f"✅ Successfully sent {len(users)} confirmation emails!")
    print("=== END MOCK EMAIL SYSTEM ===")
    
    return len(users)

def send_welcome_email(user):
    """Send welcome email to new users"""
    try:
        if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
            msg = Message(
                subject='Welcome to AI Study Buddy! 🧠',
                sender=Config.MAIL_DEFAULT_SENDER,
                recipients=[user.email]
            )
            
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #3B82F6, #8B5CF6); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🧠 Welcome to AI Study Buddy!</h1>
                    </div>
                    <div class="content">
                        <h2>Hello {user.username}!</h2>
                        <p>Welcome to AI Study Buddy - your intelligent companion for smarter studying!</p>
                        
                        <p><strong>Get started:</strong></p>
                        <ul>
                            <li>📝 Paste your study notes to generate flashcards</li>
                            <li>🎯 Study with interactive flip cards</li>
                            <li>💡 Share suggestions to help us improve</li>
                        </ul>
                        
                        <p>Happy studying! 📚</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            mail.send(msg)
            return True
        else:
            print(f"Mock welcome email sent to {user.email}")
            return True
            
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        return False
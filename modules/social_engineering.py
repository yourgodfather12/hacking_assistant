import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
import logging

logger = logging.getLogger(__name__)

def send_email(target_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = target_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, target_email, msg.as_string())
        logger.info(f"Email sent to {target_email}")
    except Exception as e:
        logger.error(f"Error sending email to {target_email}: {e}")

def run_social_engineering_attack(target_email):
    subject = "Urgent: Action Required"
    body = "Dear user, please reply to this email with your account details to avoid deactivation."
    send_email(target_email, subject, body)

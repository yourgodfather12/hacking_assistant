import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def run_social_engineering_attack(target_email):
    subject = "Urgent: Action Required"
    body = "Dear user, please reply to this email with your account details to avoid deactivation."

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
        print(f"Social engineering email sent to {target_email}")
    except Exception as e:
        print(f"Error sending social engineering email: {e}")

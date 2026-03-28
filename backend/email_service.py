import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("IntentOS")

# Configuration from environment
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMERGENCY_EMAIL_TO = os.getenv("EMERGENCY_EMAIL_TO") or GMAIL_USER

def send_emergency_email(user_info: dict, location_data: dict, analysis: dict):
    """
    Sends a high-priority emergency email with user details and location.
    """
    if not GMAIL_APP_PASSWORD or not GMAIL_USER:
        logger.error("GMAIL_USER / GMAIL_APP_PASSWORD not set. Cannot send emergency email.")
        return False

    recipient = EMERGENCY_EMAIL_TO
    if not recipient:
        logger.error("EMERGENCY_EMAIL_TO or GMAIL_USER required for recipient address.")
        return False
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = recipient
    msg['Subject'] = f"🚨 EMERGENCY: Intent detected for {user_info.get('name', 'Unknown User')}"

    # Build the body
    body = f"""
    INTENTOS EMERGENCY ALERT
    -------------------------
    User: {user_info.get('name', 'Unknown')}
    Email: {user_info.get('email', 'Unknown')}
    
    INTENT ANALYSIS:
    - Intent: {analysis.get('intent', 'N/A')}
    - Severity: {analysis.get('severity', 'High')}
    - Condition: {analysis.get('condition', 'N/A')}
    
    LOCATION DATA:
    - Coordinates: {location_data.get('lat')}, {location_data.get('lng')}
    - Elevation: {location_data.get('elevation')} meters
    - Google Maps Link: https://www.google.com/maps?q={location_data.get('lat')},{location_data.get('lng')}
    
    IMMEDIATE ACTIONS SUGGESTED:
    {chr(10).join(['- ' + a for a in analysis.get('immediate_actions', [])])}
    
    -- Sent via IntentOS AI Orchestrator
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        logger.info(f"Emergency email successfully sent to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send emergency email: {e}")
        return False

if __name__ == "__main__":
    # Local test block
    test_user = {"name": "Test User", "email": "test@example.com"}
    test_loc = {"lat": 12.9716, "lng": 77.5946, "elevation": 920}
    test_analysis = {
        "intent": "Test Emergency",
        "severity": "High",
        "condition": "Simulated hardware test",
        "immediate_actions": ["Verify email reception", "Check spam folder"]
    }
    print("Sending test mail...")
    send_emergency_email(test_user, test_loc, test_analysis)

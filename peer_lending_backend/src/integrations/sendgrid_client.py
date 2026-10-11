# peer_lending_backend/src/security/sendgrid_client.py

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "YOUR_SENDGRID_API_KEY"
FROM_EMAIL = "no-reply@peer-lending.com"

def send_email(to_email: str, subject: str, html_content: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response.status_code

"""
Sends an email notification whenever someone submits the contact form.

Uses plain SMTP (works with Gmail, Outlook, or any SMTP provider) so no
extra paid service is required. Configure it via environment variables —
see .env.example for what to fill in.

Gmail setup (most common case):
    1. Turn on 2-Step Verification on the Google account.
    2. Create an "App Password": Google Account -> Security -> App
       passwords. Choose "Mail" and generate a 16-character password.
    3. Use that app password as SMTP_PASSWORD below (not the normal
       Gmail password — Gmail blocks that over SMTP).
"""

import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")          # the email account that sends the notification
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # app password, not your normal login password
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "chhayakushwaha100@gmail.com")  # where you receive it


def send_contact_notification(name: str, email: str, message: str) -> bool:
    """Send an email to NOTIFY_EMAIL about a new contact form submission.

    Returns True if the email was sent, False if it was skipped or failed.
    Never raises — a broken mail server should not stop the form from
    saving to the database.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("[email] SMTP_USER / SMTP_PASSWORD not set — skipping email notification.")
        return False

    email_msg = EmailMessage()
    email_msg["Subject"] = f"New portfolio message from {name}"
    email_msg["From"] = SMTP_USER
    email_msg["To"] = NOTIFY_EMAIL
    email_msg["Reply-To"] = email  # reply straight to the visitor
    email_msg.set_content(
        f"You've got a new message from your portfolio contact form.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}\n"
    )

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email_msg)
        return True
    except Exception as exc:  # pragma: no cover
        print(f"[email] Failed to send contact notification: {exc}")
        return False

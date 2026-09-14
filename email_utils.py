import os
import resend

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
NOTIFY_EMAIL = os.getenv(
    "NOTIFY_EMAIL",
    "chhayakushwaha100@gmail.com"
)

resend.api_key = RESEND_API_KEY


def send_contact_notification(name: str, email: str, message: str) -> bool:

    if not RESEND_API_KEY:
        print("[email] RESEND_API_KEY not set")
        return False

    params = {
        "from": "Portfolio <onboarding@resend.dev>",
        "to": [NOTIFY_EMAIL],
        "subject": f"New portfolio message from {name}",
        "html": f"""
        <h2>New Portfolio Contact Message</h2>

        <p><strong>Name:</strong> {name}</p>

        <p><strong>Email:</strong> {email}</p>

        <p><strong>Message:</strong></p>
        <p>{message}</p>
        """,
        "reply_to": email,
    }

    try:
        response = resend.Emails.send(params)
        print("[email] Email sent successfully:", response)
        return True

    except Exception as error:
        print(f"[email] Failed to send email: {error}")
        return False
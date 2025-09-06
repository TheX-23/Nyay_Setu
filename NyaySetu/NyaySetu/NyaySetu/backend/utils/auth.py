import os
import smtplib
import ssl
from email.message import EmailMessage

def send_verification_email(recipient_email: str, verify_link: str) -> None:
    """
    Send a verification email using SMTP.
    Expects the following environment variables:
      - SMTP_HOST (optional, default smtp.gmail.com)
      - SMTP_PORT (optional, default 587)
      - SMTP_USER (required)  -> full sender email (e.g. youraccount@gmail.com)
      - SMTP_PASS (required)  -> app password or SMTP password

    For Gmail, create an App Password (recommended) and set SMTP_USER to your Gmail address
    and SMTP_PASS to the app password. Ensure SMTP_PORT=587 (TLS) or 465 (SSL) if desired.
    """
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    if not smtp_user or not smtp_pass:
        raise RuntimeError("SMTP_USER or SMTP_PASS not configured in environment")

    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))

    msg = EmailMessage()
    msg['Subject'] = 'Verify your NyaySetu account'
    msg['From'] = smtp_user
    msg['To'] = recipient_email

    text_body = (
        f"Hello,\n\n"
        f"Thank you for registering with NyaySetu.\n\n"
        f"Please verify your email by clicking the link below:\n\n{verify_link}\n\n"
        f"If you did not create an account, you can ignore this message.\n\n"
        f"— NyaySetu"
    )
    html_body = (
        "<html><body>"
        "<p>Hello,</p>"
        "<p>Thank you for registering with <b>NyaySetu</b>.</p>"
        f"<p>Please verify your email by clicking the button below:</p>"
        f"<p><a href=\"{verify_link}\" style=\"display:inline-block;padding:10px 16px;"
        "background:#1a73e8;color:#fff;border-radius:6px;text-decoration:none;\">Verify Email</a></p>"
        "<p>If you did not create an account, you can ignore this message.</p>"
        "<p>— NyaySetu</p>"
        "</body></html>"
    )

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')

    context = ssl.create_default_context()
    try:
        # Use STARTTLS for port 587, SSL for 465
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=15) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
    except Exception as e:
        # Let caller log/handle the exception
        raise
import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "aronklarson@gmail.com"         # replace with your Gmail
    msg["To"] = to_email

    # Login & Send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("aronklarson@gmail.com", "rtmf tdtn usmj dxbr")  # Use app password here
        smtp.send_message(msg)



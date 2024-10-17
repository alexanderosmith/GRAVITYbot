from dotenv import find_dotenv, load_dotenv
import os, smtplib, ssl
from email.mime.text import MIMEText

subject = "Testing Email"
body = "Hello World"

_ = load_dotenv(find_dotenv())    
sender = os.getenv("GOOGLE_APP_FROM")
password = os.getenv("GOOGLE_APP_PASS")
recipients = os.getenv("GOOGLE_APP_TO")
smtp_server = 'smtp.gmail.com'


def send_email(subject, body, sender, recipients, password, smtp_server):
    # Building the message with MIME
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, 587) as server:
    # Sending through TLS mode
        server.starttls(context=context)
        server.login(sender, password)

        server.sendmail(
            sender,
            recipients,
            msg.as_string()
        )


send_email(subject, body, sender, recipients, password, smtp_server)
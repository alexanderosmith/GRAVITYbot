from dotenv import find_dotenv, load_dotenv     # Loading env file
import os, smtplib, ssl                         # OS and server/mail protocol libraries
from email.mime.text import MIMEText            # Email Formatting

# Email Subject/Body "Hello There" Email Test
subject = "Testing Email"
body = "Hello World"

# Loading the necessary info for the email from env file
_ = load_dotenv(find_dotenv())    
sender = os.getenv("GOOGLE_APP_FROM")
password = os.getenv("GOOGLE_APP_PASS")
recipients = os.getenv("GOOGLE_APP_TO")
# Google's SMTP server location
smtp_server = 'smtp.gmail.com'

# A function that sends email
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
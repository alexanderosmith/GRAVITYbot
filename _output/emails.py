#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator: Alexander O. Smith (2024-present), aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: Oct 17, 2024
# Program Goal:
# This file sends emails and automates posts to forums that are returned from GRAVITYbot summaries.
#####################################################################################################
# NOTICE: 
# 1. For this functionality to work, you need to get an Google App password and add all the proper
# GOOGLE_APP_XXX variables in the dotenv file.
# 2. You will need to make sure that the "recipients" email(s) will accept email from the "sender."
#####################################################################################################
# DEPENDENCIES ######################################################################################
# Package Dependencies
from dotenv import find_dotenv, load_dotenv     # Loading env file
import os, smtplib, ssl                         # OS and server/mail protocol libraries
from email.mime.text import MIMEText            # Email Formatting
import markdown

def talk_email(date, body):
    # Email Subject/Body "Hello There" Email Test
    subject = "GRAVITYbot Talk Summary: " + date
    body = markdown.markdown(body)
    # TO-DO: Format email here

    return subject, body

# A function that sends email
def send_email(subject, body):
    # Loading the necessary info for the email from env file
    _ = load_dotenv(find_dotenv())    
    user = os.getenv("SMTP_USER")
    sender = user+'@syr.edu'
    host = os.getenv("SMTP_HOST")
    smtp_server = host
    password = os.getenv("SMTP_PASS")
    recipients = os.getenv("GOOGLE_APP_TO")
    
    #sender = os.getenv("GOOGLE_APP_FROM")
    #password = os.getenv("GOOGLE_APP_PASS")
    #recipients = os.getenv("GOOGLE_APP_TO")
    # Google's SMTP server location
    # If you wish to use a different email, you'll have to change this.
    #smtp_server = 'smtp.gmail.com'
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

def main(date, body):
    email = talk_email(date, body)
    send = send_email(email[0], email[1])
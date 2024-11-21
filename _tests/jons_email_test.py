import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp-relay.syr.edu"
SMTP_PORT = 587
SMTP_USER = "s-ist-ccdsmail"
SMTP_PASSWORD = "zsgtk-kl88l-6mk2o-myxjy-78ik3"

MSG_BODY = "test body"
MSG_SUBJECT = "test subject"
MSG_FROM = "aosmith@syr.edu"
MSG_TO = "aosmith@syr.edu"

## --------------------
## Our Message
## --------------------
msg = MIMEText(MSG_BODY)
msg['Subject'] = MSG_SUBJECT
msg['From'] = MSG_FROM
msg['To'] = MSG_TO
## --------------------

## --------------------
## Connect and send
## --------------------
server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASSWORD)
server.sendmail(MSG_FROM, [MSG_TO], msg.as_string())
server.quit()
## --------------------

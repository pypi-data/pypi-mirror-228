import smtplib
import re
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from config import EMAIL_ADDRESS, EMAIL_PASSWORD


def getFromConfig():
    receiver_emails = []
    sender_email = EMAIL_ADDRESS
    sender_password = EMAIL_PASSWORD

    max_email = int(input("How many Receiver Emails: "))

    while max_email > 0:
        receiver_emails.append(input("Receiver: "))
        max_email -= 1

    subject = input("Subject: ")
    message = input("Message: ")

    return sender_email, sender_password, receiver_emails, subject, message


def MimeObject(sender_email, receiver_emails, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    return msg


def SMPTSending(sender, receiver_emails, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = EMAIL_ADDRESS
    smtp_password = EMAIL_PASSWORD

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    try:
        server.login(smtp_username, smtp_password)
    except smtplib.SMTPAuthenticationError as e:
        error_message = e.smtp_error.decode() if hasattr(e, 'smtp_error') else str(e)
        if "BadCredentials" in error_message:
            print("SMTP Authentication Error: The username or password is not accepted.")
        else:
            print("SMTP Authentication Error:", error_message)
    except Exception as e:
        print("An error occurred:", e)

    for receiver_email in receiver_emails:
        if re.match(gmail_email_pattern, receiver_email):
            server.sendmail(sender, receiver_email, message.as_string())
        else:
            print("Invalid Receiver Email:", receiver_email)

    server.quit()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    email = ""
    password = ""
    subj = ""
    msg = ""

    # Email Configuration
    gmail_email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if re.match(gmail_email_pattern, EMAIL_ADDRESS):
        email, password, receiver, subj, msg = getFromConfig()
        mimeMSG = MimeObject(email, receiver, subj, msg)
        SMPTSending(email, receiver, mimeMSG)
    else:
        print("Invalid Sender Email.")

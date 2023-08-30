import smtplib
import re
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from config import EMAIL_ADDRESS, EMAIL_PASSWORD


def getFromConfig():
    sender_email = EMAIL_ADDRESS
    sender_password = EMAIL_PASSWORD

    receiver_email = str(input("Receiver Email: "))
    subject = str(input("Subject: "))
    message = str(input("Message: "))

    return sender_email, sender_password, receiver_email, subject, message


def MimeObject(sender_email, receiver_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    return msg


def SMPTSending(sender, receiver_email, message):
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

    gmail_email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if re.match(gmail_email_pattern, receiver_email):
        server.sendmail(sender, receiver_email, message.as_string())
    else:
        print("Invalid Receiver Email.")

    server.quit()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    email = ""
    password = ""
    receiver = ""
    subj = ""
    msg = ""

    # Email Configuration
    gmail_email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if re.match(gmail_email_pattern, EMAIL_ADDRESS):
        email, password, receiver, subj, msg = getFromConfig()
    else:
        print("Invalid Sender Email.")

    # Object for the Email
    mimeMSG = MimeObject(email, receiver, subj, msg)

    # STAGE 1: Connect to the SMTP server
    # STAGE 2: Start the server connection
    # STAGE 3: Log in to your email account
    # STAGE 4: Send the email
    # STAGE 5: Quit the server
    SMPTSending(email, receiver, mimeMSG)

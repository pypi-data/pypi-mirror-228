# EmailSender Python Script

**Author:** Harold Edsel F. Cabaluna

The *EmailSender* Python script is a tool designed to simplify the process of sending emails using Python. This script leverages the power of Python's `smtplib` library to send emails programmatically, making it useful for various applications such as automating notifications, sending reports, or communicating with users.

## Features

- Send emails to one or more recipients.
- Support for plain text and HTML email content.
- Attachment functionality for sending files along with emails.

## Prerequisites

Before using the EmailSender script, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- A valid email account from which you want to send emails.
- Internet connectivity to establish a connection with the email server.

## Installation

1. Clone or download the repository to your local machine. git clone https://github.com/your_username/EmailSender.git

2. Navigate to the project directory:
```cd EmailSender```

3. Install the required dependencies:
```pip install -r requirements.txt```

## Usage

1. Open the `config.py` file and provide your email account details:

```python
# Email Account Configuration
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
```

1. Customize the main.py script to set the recipient's email address, subject, message, and attachments (if needed).

2. Run the script:
```python EmailSender/sender.py```

3. The script will establish a connection to the email server and send the email with the specified content and attachments.

## Example

```python
from EmailSender_GhostPoltergeist import config

email_sender = config.EMAIL_ADDRESS

recipient = "recipient@example.com"

subject = "Hello from EmailSender_GhostPoltergeist!"
message = "This is a test email sent using the EmailSender_GhostPoltergeist script."

attachment_path = "path/to/attachment.pdf"
email_sender.attach_file(attachment_path)

email_sender.send_email(recipient, subject, message)
```

## SMTP Setup
```
Generate an Application-Specific Password:

1. Go to your Google Account settings: https://myaccount.google.com/

2. In the "Security" section, find the "Signing in to Google" option.

3. Click on "App passwords."

4. Select "Mail" and "Other (Custom name)" from the dropdowns.

5. Enter a custom name for your app, like "EmailSender."

6. Click the "Generate" button.

7. Google will provide you with a generated password. Copy this password.****
```

## Use the Application-Specific Password in your Code
In config.py script, replace the EMAIL_PASSWORD variable
with the generated application-specific password you obtained from Google:
```python
EMAIL_PASSWORD = 'your_generated_app_password'
```

## Contributions
Contributions to the EmailSender Python script are welcome! If you find any issues or want to enhance its features, feel free to create a pull request.

## License
This project is licensed under the MIT License - see the LICENSE.txt file for details.

Feel free to reach out to me at EdselCabaluna21@gmail.com for any questions or suggestions! Your feedback is greatly appreciated.

   

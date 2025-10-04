import smtplib
from email.mime.text import MIMEText

class GMail:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.server.login(self.email, self.password)

    def send(self, message):
        self.server.send_message(message.msg)
        self.server.quit()
        print("✅ Email sent successfully!")

class Message:
    def __init__(self, to, subject, text):
        msg = MIMEText(text)
        msg["To"] = to
        msg["Subject"] = subject
        self.msg = msg

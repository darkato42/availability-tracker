import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailService:

    def __init__(self, from_address="dont5pannnne@gmail.com", password=""):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.from_address = from_address
        self.password = password

    def send(self, to_address: str, subject: str, body: str):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.from_address, self.password)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_address
        msg["To"] = to_address
        msg.attach(MIMEText(body, 'plain'))

        result = service.sendmail(self.from_address, to_address, msg.as_string())

        service.quit()


if __name__ == '__main__':
    mails = input("Enter recipient email: ")
    subject = input("Enter subject: ")
    body = input("Enter content: ")
    password = input("Enter Gmail App Password: ")
    mail_service = MailService(password=password)
    mail_service.send(mails, subject, body)

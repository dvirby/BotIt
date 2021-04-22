import smtplib
from email.header import Header
from email.mime.text import MIMEText

from APIs.ExternalAPIs.Mail import mail_secret


class MailClient:
    def __init__(self, user=mail_secret.GMAIL_USER, password=mail_secret.GMAIL_PASSWORD):
        self.server: smtplib.SMTP_SSL = None
        self.user = user
        self.password = password

    def connect(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(self.user, self.password)

    def close(self):
        self.server.close()

    def send_mail(self, to, subject, content, text_type="plain"):
        # message = 'Subject: {}\n\n{}'.format(subject, content)
        msg = MIMEText(content, text_type, _charset="UTF-8")
        msg['Subject'] = Header(subject, "utf-8")
        self.server.sendmail(mail_secret.GMAIL_USER, to, msg.as_string())

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class SendMessage:
    def __init__(self, email_sender, password):
        self.email_sender = email_sender
        self.password = password
        self.msg = MIMEMultipart()


    def subject(self, subject):
        self.msg['subject'] = subject       #adding subject of the message


    def body(self, content):
        self.msg.attach(MIMEText(content, 'plain'))      #adding the body text to the message


    def attach(self, filename, path):
        attachment = open(path, 'rb')              #opening the attachment 

        payload = MIMEBase('application', 'octet-stream')       
        payload.set_payload(attachment.read())                  #encoding the attachment into base64
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment; filename = %s' % filename)

        self.msg.attach(payload)         #adding the attachment to the message


    def send_mail(self, email_receiver):

        self.msg['From'] = self.email_sender
        self.msg['To'] = email_receiver

        session = smtplib.SMTP('smtp.gmail.com', 587)           #starting SMTP session
        session.starttls()                                      #starting TLS for security
        session.login(self.email_sender, self.password)         #authentication

        text = self.msg.as_string()          #converting the msg to a string

        session.sendmail(self.email_sender, email_receiver, text)          #sending the mail
        session.quit()          #terminating the session

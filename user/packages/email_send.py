import os
import smtplib

from email.message import EmailMessage

def send_email(EMAIL_ADDRESS,EMAIL_PASSWORD,contacts,subject,body,files):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(contacts)
    msg.set_content(body)#.encode('utf-8').strip())
    for file in files:
        with open(file,'rb') as f:
            file_data=f.read()
            head, tail = os.path.split(file)
            file_name=tail
        print(msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

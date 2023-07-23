from email.message import EmailMessage
import ssl
import smtplib
import random

email_sender = 'bissfit2fa@gmail.com'
email_password = ''
email_receiver = ''
verification_code = random.randint(99999,1000000) #pseudo random, TODO

with open('config') as f:
    email_password = f.readline()

subject = 'New sign in to 2FADemo'
body = """
Hi, your verification code is  {}
""".format(verification_code)

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
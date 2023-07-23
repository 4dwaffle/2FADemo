from email.message import EmailMessage
import ssl
import smtplib
import random

email_sender = 'bissfit2fa@gmail.com'
email_password = ''
verification_code = random.randint(99999,1000000) #pseudo random, TODO
with open('config') as f:
    email_password = f.readline()

def send_email(receiver, code):
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

def login(email, password) -> bool: # TODO
    return True

if __name__ == '__main__':
    email_receiver = input("Email: ")
    password_receiver = input("Password: ")

    if login(email_receiver, password_receiver):
        send_email(email_receiver, verification_code)
        receiver_code = input("Verification Code: ")
        if receiver_code == str(verification_code):
            print("Welcome back")
        else:
            print("Wrong verification code")
    else:
        print("Wrong login credentials")

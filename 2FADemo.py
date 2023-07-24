from getpass import getpass
from email.message import EmailMessage
import ssl
import smtplib
import random
import hashlib
import sqlite3

email_sender = 'bissfit2fa@gmail.com'
email_password = ''
verification_code = random.randint(99999,1000000)
with open('config') as f:
    email_password = f.readline()

def connect_db():
    return sqlite3.connect("login.db")


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

def login(email, password) -> bool:
    hash = get_hash(password)
    hash_from_db = fetch_pw(email)
    
    if hash == hash_from_db:
        return True
    else:
        return False

def get_hash(password):
    hash_object = hashlib.md5(bytes(str(password), encoding='UTF-8'))
    return hash_object.hexdigest()

def fetch_pw(email):
    cursor = connect_db().cursor()
    try:
        cursor.execute("select pwhash from credentials where email='{}' limit 1".format(email))
        pwhash = cursor.fetchone()
        if pwhash != None: 
            return pwhash[0]
        else:
            return {'status' : '400'}
    except Exception as e:
        return {'Error', str(e)}

def save_credentials(email, pwhash):
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("INSERT INTO credentials(email, pwhash) VALUES ('{}', '{}')".format(email, pwhash))
    connect.commit()

def email_exists(email) -> bool:
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("select email from credentials where email='{}' limit 1".format(email))
    if cursor.fetchone() != None:
        return True
    else:
        return False
        
def create_account(email):
    print("Account with this email address doesnt exist, create a new one:")
    while True:
        password1 = get_hash(getpass("Your new password: "))
        password2 = get_hash(getpass("Password again: "))
        if password1 == password2:
            save_credentials(email, password1)
            print("Great, your account was created. You can now sign in.")
            return
        else:
            print("Passwords does not mach, try again.")

if __name__ == '__main__':
    email_receiver = input("Email: ")
    if not email_exists(email_receiver):
        create_account(email_receiver)

    password_receiver = getpass("Password: ")
    if login(email_receiver, password_receiver):
        send_email(email_receiver, verification_code)
        receiver_code = input("Verification Code: ")
        if receiver_code == str(verification_code):
            print("Welcome back")
        else:
            print("Wrong verification code")
    else:
        print("Wrong login credentials")

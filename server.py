import random
import socket
import os
from dotenv import load_dotenv
from smtplib import SMTP
import re

load_dotenv()

email_checker = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
host = '127.0.0.1'
port = 5000
admin_data = (os.getenv("EMAIL_LOGIN"), os.getenv("EMAIL_PASSWORD"))

smtp_client = SMTP(os.getenv("SMTP_HOST") + ":" + os.getenv("SMTP_PORT"))
smtp_client.starttls()
smtp_client.login(admin_data[0], admin_data[1])


def generate_message(message):
    return """Subject: [Ticket#""" + str(random.randrange(1000)) + """] Mailer \n""" + message


def parse_data(response):
    split = response.decode().split("|", maxsplit=2)
    if len(split) != 2:
        return b'COUNT_ARGS'
    if not re.match(email_checker, split[0]):
        return b'EMAIL_NOT_RIGHT'

    message = generate_message(split[1])
    try:
        smtp_client.sendmail(admin_data[0], split[0], message)
        smtp_client.sendmail(admin_data[0], admin_data[0], message)
        print('success')
    except Exception as exc:
        print('error')

    return b'OK'


print('start')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print('connected')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(parse_data(data))
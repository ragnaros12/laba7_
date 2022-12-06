import time
from imaplib import IMAP4_SSL
import os
from dotenv import load_dotenv
import email
import re
import os
from dotenv import load_dotenv

load_dotenv()

updates = os.getenv('PERIOD_CHECK')
regex = re.compile("[Ticket#[\d]+] Mailer")


with IMAP4_SSL(os.getenv("IMAP_HOST"), int(os.getenv("IMAP_PORT"))) as M:
    rc, resp = M.login(os.getenv("EMAIL_LOGIN"), os.getenv("EMAIL_PASSWORD"))

    while True:
        M.select()
        typ, data = M.uid("search", 'UNSEEN')
        with open('error_request.log', 'a') as errors, open('success_request.log', 'a') as success:
            for i in data[0].split():
                    code, msg = M.uid('fetch', i, "(RFC822)")
                    decoded_email = email.message_from_string(msg[0][1].decode())
                    payload = decoded_email.get_payload()

                    payload = payload if isinstance(payload, str) else ''.join(map(str, payload))

                    if re.match(regex, decoded_email['Subject']):
                        success.write(decoded_email['Subject'] + " " + payload + "\n")
                    else:
                        errors.write(payload)
        print('success write')
        time.sleep(int(updates))

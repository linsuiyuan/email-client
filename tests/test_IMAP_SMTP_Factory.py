import json
import os
from dotenv import load_dotenv
from EmailClients import IMAP_SMTP_Factory


def test_imap_login():
    load_dotenv(dotenv_path='.env.163')  
    username = os.getenv('USERNAME')
    print('\n', username)
    with IMAP_SMTP_Factory.create_imap(username) as client:
        typ, dat = client.login(username, os.getenv('PASSWORD'))
        print(typ, dat)
import json
import os
from dotenv import load_dotenv
import pytest
from EmailClients import Netease_IMAP4_SSL


def test_imap_client_login():
    load_dotenv(dotenv_path='.env.163')  # 你可以指定.env文件路径
    email_host_str = os.getenv('EMAIL_HOST')
    email_host = json.loads(email_host_str)
    with Netease_IMAP4_SSL(email_host['imap']) as client:
        typ, dat = client.login(os.getenv('USERNAME'),os.getenv('PASSWORD'))
        print(typ, dat)
        
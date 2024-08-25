import json
import os
import sys
import pytest
from dotenv import load_dotenv
from EmailClients import EmailClient


@pytest.fixture(scope='module', autouse=True)
def email_client():
    load_dotenv(dotenv_path='.env.com')  # 你可以指定.env文件路径
    email_host_str = os.getenv('EMAIL_HOST')
    email_host = json.loads(email_host_str)
    client = EmailClient(username=os.getenv('USERNAME'),
                         password=os.getenv('PASSWORD'),
                         email_host=email_host)
    print("\n", client.email_host, client.username, client.password)
    yield client


def test_read_email(email_client):
    try:
        pass
        emails = email_client.read_emails(criteria="ALL")
        print(json.dumps(emails, ensure_ascii=False))
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected exception: {e}")


def test_send_email(email_client):
    print(os.getenv('RECIPIENT'))
    result, msg = email_client.send_email(to=os.getenv('RECIPIENT'), subject="测试", content="测试")
    print(msg)
    assert result == True

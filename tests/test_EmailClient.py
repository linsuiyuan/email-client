import json
import os
import pytest
from dotenv import load_dotenv
from EmailClients import EmailClient


@pytest.fixture(scope='module', autouse=True)
def email_client():
    load_dotenv(dotenv_path='.env.163')  # 你可以指定.env文件路径
    client = EmailClient(username=os.getenv('USERNAME'),
                         password=os.getenv('PASSWORD'))
    print("\n", client.username, client.password)
    yield client


def test_read_email(email_client):
    try:
        pass
        emails = email_client.read_emails(criteria="ALL")
        print(json.dumps(emails, ensure_ascii=False))
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected exception: {e}")

def test_read_unseen_email(email_client):
    try:
        pass
        emails = email_client.read_emails(criteria="UNSEEN", seen=True)
        print(json.dumps(emails, ensure_ascii=False))
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected exception: {e}")

def test_read_and_delete_email(email_client):
    try:
        pass
        emails = email_client.read_emails(criteria="UNSEEN", delete=True)
        print(json.dumps(emails, ensure_ascii=False))
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected exception: {e}")

def test_send_email(email_client):
    print(os.getenv('RECIPIENT'))
    result, msg = email_client.send_email(to=os.getenv('RECIPIENT'), subject="测试2", content="测试2")
    print(msg)
    assert result == True

def test_send_email_with_attachments(email_client):
    print(os.getenv('RECIPIENT'))
    attachments = ['/Users/willowlin/Downloads/hehe.txt', 
                   '/Users/willowlin/Downloads/00__55.png']
    result, msg = email_client.send_email(to=os.getenv('RECIPIENT'), 
                                          subject="测试3", 
                                          content="测试3", 
                                          attachments=attachments)
    print(msg)
    assert result == True
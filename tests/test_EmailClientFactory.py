import json
import os
from dotenv import load_dotenv
import pytest
from EmailClients import EmailClient, EmailClientFactory


@pytest.fixture(scope='module', autouse=True)
def email_client():
    load_dotenv(dotenv_path='../.env.com')  # 你可以指定.env文件路径
    client: EmailClient = EmailClientFactory.generate_email_client(username=os.getenv('USERNAME'),
                                                                   password=os.getenv('PASSWORD'))
    print("\n", client.email_host, client.username, client.password)
    yield client


def test_read_email(email_client):
    emails = email_client.read_emails("ALL")
    print(emails)
    assert emails != []


def test_read_unseen_email(email_client):
    emails = email_client.read_emails("UNSEEN", seen=True)
    print(emails)
    assert emails != []


def test_read_and_delete_email(email_client):
    emails = email_client.read_emails("UNSEEN", delete=True)
    print(emails)
    assert emails != []


def test_send_email(email_client):
    print(os.getenv('RECIPIENT'))
    result, msg = email_client.send_email(to=os.getenv('RECIPIENT'),
                                          subject="测试2",
                                          content="测试2")
    print(msg)
    assert result == True


def test_send_email_with_attachment(email_client):
    print(os.getenv('RECIPIENT'))
    attachments = ["/Users/willowlin/Downloads/正念.png",
                   "/Users/willowlin/Downloads/hehe.txt"]
    result, msg = email_client.send_email(to=os.getenv('RECIPIENT'),
                                          subject="测试7",
                                          content="测试7",
                                          attachments=attachments)
    print(msg)
    assert result == True

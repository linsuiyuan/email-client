import pytest  # noqa
from unittest.mock import MagicMock, patch
from emlclient.emailclient import EmailClient


@pytest.fixture
def email_client():
    """邮件实例"""
    return EmailClient("test@example.com", "password123")


@pytest.fixture
def mock_email_message():
    """创建一个完整的测试邮件"""
    return b"""From: sender@example.com
To: recipient@example.com
Subject: Test Subject
Date: Thu, 1 Jan 2023 00:00:00 +0000
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0

This is a test email body."""


@pytest.fixture
def mock_email_message_minimal():
    """创建一个最小化的邮件消息，包含可能为空的header"""
    return b"""From: test@example.com
To: 
Subject: Test
Date: Thu, 1 Jan 2023 00:00:00 +0000
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0

Test content"""


def test_parse_email(email_client, mock_email_message):
    """测试完整邮件解析功能"""
    result = email_client._parse_email(mock_email_message)

    assert result["sender"] == "sender@example.com"
    assert result["recipient"] == "recipient@example.com"
    assert result["subject"] == "Test Subject"
    assert "This is a test email body" in result["body"]


def test_parse_email_minimal(email_client, mock_email_message_minimal):
    """测试处理最小化邮（某些header可能为空）"""
    result = email_client._parse_email(mock_email_message_minimal)

    assert result["sender"] == "test@example.com"
    assert result.get("recipient") == ""  # 收件人可能为空
    assert result["subject"] == "Test"
    assert "Test content" in result["body"]


@patch('emlclient.emailclient.IMAP_SMTP_Factory')
def test_read_emails(mock_factory, email_client, mock_email_message_minimal):
    """测试读取邮件功能"""
    # 设置模拟对象
    mock_imap = MagicMock()
    mock_factory.create_imap.return_value.__enter__.return_value = mock_imap

    # 模拟邮件搜索结果
    mock_imap.search.return_value = (None, [b'1'])
    
    # IMAP fetch 返回格式：(response_code, [(msg_num, (flags, msg_data))])
    mock_imap.fetch.return_value = (None, [
        (b'1', mock_email_message_minimal)  # 简化的返回格式
    ])

    # 执行测试
    emails = email_client.read_emails("ALL", limit=1)

    # 验证结果
    assert len(emails) == 1
    assert emails[0]["sender"] == "test@example.com"
    assert emails[0]["subject"] == "Test"

    # 验证调用
    mock_imap.search.assert_called_once()
    mock_imap.fetch.assert_called_once()


@patch('emlclient.emailclient.IMAP_SMTP_Factory')
def test_send_email(mock_factory, email_client):
    """测试发送邮件功能"""
    # 设置模拟对象
    mock_smtp = MagicMock()
    mock_factory.create_smtp.return_value.__enter__.return_value = mock_smtp

    # 执行测试
    result = email_client.send_email(
        to="recipient@example.com",
        subject="Test Subject",
        content="Test Content"
    )

    # 验证结果
    assert result == (True, "发送成功")
    mock_smtp.starttls.assert_called_once()
    mock_smtp.login.assert_called_once_with(
        user="test@example.com",
        password="password123"
    )
    mock_smtp.send_message.assert_called_once()

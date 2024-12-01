import pytest  # noqa
from unittest.mock import patch
from emlclient.imap_smtp_factory import IMAP_SMTP_Factory


def test_create_imap_163():
    """测试创建网易邮箱的 IMAP 连接"""
    with patch('emlclient.imap_smtp_factory.Netease_IMAP4_SSL') as mock_imap:
        email = "test@163.com"
        imap = IMAP_SMTP_Factory.create_imap(email)

        # 验证使用了正确的主机创建连接
        mock_imap.assert_called_once_with('imap.163.com')
        assert imap == mock_imap.return_value


def test_create_imap_qq():
    """测试创建 QQ 邮箱的 IMAP 连接"""
    with patch('emlclient.imap_smtp_factory.IMAP4_SSL') as mock_imap:
        email = "test@qq.com"
        imap = IMAP_SMTP_Factory.create_imap(email)

        # 验证使用了正确的主机创建连接
        mock_imap.assert_called_once_with('imap.qq.com')
        assert imap == mock_imap.return_value


def test_create_imap_unknown():
    """测试创建未知邮箱的 IMAP 连接"""
    with pytest.raises(Exception) as exc_info:
        IMAP_SMTP_Factory.create_imap("test@unknown.com")
    assert "该邮箱未设置服务器" in str(exc_info.value)


def test_create_smtp():
    """测试创建 SMTP 连接"""
    with patch('emlclient.imap_smtp_factory.SMTP') as mock_smtp:
        email = "test@qq.com"
        smtp = IMAP_SMTP_Factory.create_smtp(email)

        # 验证使用了正确的主机创建连接
        mock_smtp.assert_called_once_with(host='smtp.qq.com')
        assert smtp == mock_smtp.return_value


def test_create_smtp_unknown():
    """测试创建未知邮箱的 SMTP 连接"""
    with pytest.raises(Exception) as exc_info:
        IMAP_SMTP_Factory.create_smtp("test@unknown.com")
    assert "该邮箱未设置服务器" in str(exc_info.value)

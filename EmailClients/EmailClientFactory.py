from EmailClients import EmailClient
from EmailClients import NeteaseEmailClient


class EmailClientFactory:
    domain_to_host = {
        '139.com': {'imap': 'imap.139.com', 'smtp': 'smtp.139.com'},
        'qq.com': {'imap': 'imap.qq.com', 'smtp': 'smtp.qq.com'},
        'gmail.com': {'imap': 'imap.gmail.com', 'smtp': 'smtp.gmail.com'},
        'outlook.com': {'imap': 'outlook.office365.com', 'smtp': 'smtp-mail.outlook.com'},
        'icloud.com': {'imap': 'imap.mail.me.com', 'smtp': 'smtp.mail.me.com'},

        '163.com': {'imap': 'imap.163.com', 'smtp': 'smtp.163.com'},
    }

    @staticmethod
    def generate_email_client(username: str, password: str) -> EmailClient:
        """根据传入的邮件地址，选择相应的imap和smtp服务器，返回相应的EmailClient

        Args:
            username (str): 邮件地址
            password (str): 邮件密码

        Raises:
            Exception: 如果没有相应的服务器，则抛出异常

        Returns:
            EmailClient: EmailClient
        """
        domain = username.split('@')[-1]
        if domain not in EmailClientFactory.domain_to_host:
            raise Exception(f'该邮箱未设置服务器：{username}')

        email_host = EmailClientFactory.domain_to_host.get(domain)
        if domain == '163.com':
            client = NeteaseEmailClient(username, password, email_host)
        else:
            client = EmailClient(username, password, email_host)
        return client

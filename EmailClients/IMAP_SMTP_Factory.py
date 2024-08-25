from smtplib import SMTP
from imaplib import IMAP4_SSL
from EmailClients import Netease_IMAP4_SSL

class IMAP_SMTP_Factory:
    domain_to_host = {
        '139.com': {'imap': 'imap.139.com', 'smtp': 'smtp.139.com'},
        'qq.com': {'imap': 'imap.qq.com', 'smtp': 'smtp.qq.com'},
        'gmail.com': {'imap': 'imap.gmail.com', 'smtp': 'smtp.gmail.com'},
        'outlook.com': {'imap': 'outlook.office365.com', 'smtp': 'smtp-mail.outlook.com'},
        'icloud.com': {'imap': 'imap.mail.me.com', 'smtp': 'smtp.mail.me.com'},

        '163.com': {'imap': 'imap.163.com', 'smtp': 'smtp.163.com'},
    }

    @staticmethod
    def create_imap(username) -> IMAP4_SSL:
        domain = username.split('@')[-1]
        if domain not in IMAP_SMTP_Factory.domain_to_host:
            raise Exception(f'该邮箱未设置服务器：{username}')

        email_host = IMAP_SMTP_Factory.domain_to_host.get(domain)
        if domain == '163.com':
            imap = Netease_IMAP4_SSL(email_host['imap'])
        else:
            imap = IMAP4_SSL(email_host['imap'])
        return imap
    
    @staticmethod
    def create_smtp(username) -> SMTP:
        domain = username.split('@')[-1]
        if domain not in IMAP_SMTP_Factory.domain_to_host:
            raise Exception(f'该邮箱未设置服务器：{username}')

        email_host = IMAP_SMTP_Factory.domain_to_host.get(domain)
        smtp = SMTP(host=email_host['smtp'])
        return smtp
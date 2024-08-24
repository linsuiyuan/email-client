import email
from email.header import decode_header
import json
import os
import imaplib
import smtplib

class IMAP4_SSL_With_Ctx(imaplib.IMAP4_SSL):
    """包装 imaplib.IMAP4_SSL，使其可以使用 with 语句"""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

class EmailClient:

    def __init__(self, username: str, password: str, email_host: str):
        self.username = username
        self.password = password
        self.email_host = email_host
    
    def _parse_email(self, raw_email):

        # 解析邮件的主要部分
        def decode_mime_words(mime_words):
            decoded_words = []
            for word, charset in decode_header(mime_words):
                if isinstance(word, bytes):
                    word = word.decode(charset or 'utf-8')
                decoded_words.append(word)
            return ''.join(decoded_words)
        
        # 解析邮件
        msg = email.message_from_bytes(raw_email)

        # 提取邮件的基本信息
        from_address = decode_mime_words(msg['From'])
        to_address = decode_mime_words(msg['To'])
        subject = decode_mime_words(msg['Subject'])
        date = msg['Date']

        # 遍历邮件的每个部分
        body_parts = []
        for part in msg.walk():
            content_type = part.get_content_type()
            charset = part.get_content_charset()
            
            # 如果部分是文本
            if content_type == "text/plain":
                if charset is None:
                    charset = 'utf-8'
                body = part.get_payload(decode=True).decode(charset)
                body_parts.append(body)
                # 这里暂时只取其中一部分
                break

            # 如果部分是 HTML
            elif content_type == "text/html":
                if charset is None:
                    charset = 'utf-8'
                body = part.get_payload(decode=True).decode(charset)
                body_parts.append(body)
                break

            
        email_obj = {
                'sender': from_address,
                'recipient': to_address,
                'subject': subject,
                'date': date,
                'body': '\n'.join(body_parts),
            }
        return email_obj

    def read_emails(self, criteria: str, mailbox="INBOX", limit=1):
        try:
            with IMAP4_SSL_With_Ctx(self.email_host) as mail:
                mail.login(self.username, self.password)
                
                mail.select(mailbox=mailbox)
                
                # 搜索邮件
                _, data = mail.search(None, criteria)
                
                email_ids = data[0].split()
                # 根据限制过滤个数
                email_ids = email_ids[:limit]

                email_objects = []
                
                # 获取邮件
                for email_id in email_ids:
                    _, msg_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    email_object = self._parse_email(raw_email=raw_email)
                    email_objects.append(email_object)

                return email_objects
        except Exception as ex:
            raise ex
            # return False, f"读取邮件失败：{ex}"


if __name__ == '__main__':
    client = EmailClient(username=os.getenv('USERNAME'),
                         password=os.getenv('PASSWORD'),
                         email_host=os.getenv('EMAIL_HOST'))
    emails = client.read_emails(criteria="UNSEEN")
    print(json.dumps(emails, ensure_ascii=False))
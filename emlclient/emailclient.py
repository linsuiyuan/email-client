import email
from email.header import decode_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

from .imap_smtp_factory import IMAP_SMTP_Factory


class EmailClient:
    """邮件客户端，可接收和发送邮件"""

    def __init__(self, username: str, password: str):
        """初始化

        Args:
            username (str): 邮件地址
            password (str): 邮件密码
        """
        self.username = username
        self.password = password

    def _parse_email(self, raw_email) -> Dict:
        """对原始邮件进行解析

        Args:
            raw_email (_type_): 原始邮件

        Returns:
            dict: 含有邮件主要信息的dict
        """

        # 解析邮件的主要部分
        def _decode_mime_words(mime_words):
            decoded_words = []
            for word, charset_ in decode_header(mime_words):
                if isinstance(word, bytes):
                    word = word.decode(charset_ or 'utf-8')
                decoded_words.append(word)
            return ''.join(decoded_words)

        # 解析邮件
        msg = email.message_from_bytes(raw_email)

        # 提取邮件的基本信息
        from_address = _decode_mime_words(msg['From'])
        to_address = _decode_mime_words(msg['To'])
        subject = _decode_mime_words(msg['Subject'])
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

    def read_emails(self, criteria: str, mailbox="INBOX", limit=1, seen=False, delete=False) -> List[Dict]:
        """读取邮件主方法

        Args:
            criteria (str): 查询邮件的条件。支持以下格式:
                - 'ALL': 所有邮件
                - 'UNSEEN': 未读邮件
                - 'SEEN': 已读邮件
                - 'FROM "someone@example.com"': 来自特定发件人的邮件
                - 'TO "someone@example.com"': 发送给特定收件人的邮件
                - 'SUBJECT "test"': 主题包含特定文字的邮件
                - 'SINCE "01-Jan-2020"': 某个日期之后的邮件
                - 'BEFORE "01-Jan-2020"': 某个日期之前的邮件
                - 'LARGER 1000': 大于1000字节的邮件
                - 'SMALLER 1000': 小于1000字节的邮件
                多个条件可以组合使用，如: 'UNSEEN SUBJECT "test"'
            mailbox (str, optional): 邮件文件夹. 默认 "INBOX".
            limit (int, optional): 数量限制. 默认 1.
            seen (bool, optional): 标记已读. 默认 False.
            delete (bool, optional): 删除邮件. 默认 False.

        Raises:
            ex: 读取邮件出错则抛出异常

        Returns:
            list[dict]: 邮件列表
        """
        try:
            with IMAP_SMTP_Factory.create_imap(self.username) as mail:
                mail.login(self.username, self.password)

                mail.select(mailbox=mailbox)

                # 搜索邮件
                _, data = mail.search(None, criteria)

                email_ids = data[0].split()
                # 根据限制过滤个数
                if limit > 0:
                    email_ids = email_ids[:limit]

                email_objects = []

                # 获取邮件
                for email_id in email_ids:
                    _, msg_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    email_object = self._parse_email(raw_email=raw_email)
                    email_objects.append(email_object)

                # 如果要删除邮件就不需要标记已读了，所以这里使用if elif
                if delete:
                    for email_id in email_ids:
                        mail.store(email_id, '+FLAGS', '\\Deleted')  # 标记邮件为删除
                        mail.expunge()  # 永久删除已标记的邮件
                elif seen:
                    for email_id in email_ids:
                        mail.store(email_id, "+FLAGS", "\\Seen")

                return email_objects
        except Exception as ex:
            raise ex

    def send_email(self, to: str, subject: str, content: str, attachments=None):
        """发送邮件

        Args:
            to (str): 接收人
            subject (str): 主题
            content (str): 邮件内容
            attachments (_type_, optional): 邮件附件. 默认 None.

        Raises:
            ex: 发送邮件失败则抛出异常

        Returns:
            _type_: 发送邮件结果
        """
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        # 如果有附件，则添加附件
        if attachments:
            for filename in attachments:
                with open(filename, 'rb') as fr:
                    part = MIMEApplication(fr.read())
                    part.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(part)

        try:
            with IMAP_SMTP_Factory.create_smtp(self.username) as server:
                server.starttls()  # 开启TLS加密
                server.login(user=self.username, password=self.password)
                server.send_message(msg)
                return True, "发送成功"
        except Exception as ex:
            raise ex

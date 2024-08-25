import imaplib
from EmailClients import EmailClient


class NeteaseEmailClient(EmailClient):

    def read_email_login(self, mail):
        """重载父类相应的方法，使163邮箱能进行特定的登录配置

        Args:
            mail (_type_): imap客户端
        """
        mail.login(self.username, self.password)
        imaplib.Commands["ID"] = ('AUTH',)
        args = ("name", self.username, "contact", self.username, "version", "1.0.0", "vendor", "myclient")
        mail._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))

import imaplib
from imaplib import IMAP4_SSL

class Netease_IMAP4_SSL(IMAP4_SSL):

    def login(self, user, password):
        """重写父类 login，根据163邮件的特殊需求进行相应的配置

        Args:
            user (str): 邮件地址
            password (str): 邮件密码或秘钥

        Returns:
            _type_: 登录信息和数据
        """
        typ, dat = super().login(user, password)
        imaplib.Commands["ID"] = ('AUTH',)
        args = ("name", user, "contact", user, "version", "1.0.0", "vendor", "myclient")
        self._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))
        return typ, dat

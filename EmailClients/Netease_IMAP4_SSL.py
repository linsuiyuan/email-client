import imaplib
from imaplib import IMAP4_SSL

class Netease_IMAP4_SSL(IMAP4_SSL):

    def login(self, user, password):
        typ, dat = super().login(user, password)
        imaplib.Commands["ID"] = ('AUTH',)
        args = ("name", user, "contact", user, "version", "1.0.0", "vendor", "myclient")
        self._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))
        return typ, dat

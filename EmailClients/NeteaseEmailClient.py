import imaplib
from EmailClients import EmailClient

class NeteaseEmailClient(EmailClient):

    def read_email_login(self, mail):
        mail.login(self.username, self.password)
        imaplib.Commands["ID"] = ('AUTH',)
        args = ("name", self.username, "contact", self.username, "version", "1.0.0", "vendor", "myclient")
        mail._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))



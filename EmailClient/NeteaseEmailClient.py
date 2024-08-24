import imaplib
import json
import os
from EmailClient import EmailClient

class NeteaseEmailClient(EmailClient):

    def read_email_login(self, mail):
        mail.login(self.username, self.password)
        imaplib.Commands["ID"] = ('AUTH',)
        args = ("name", self.username, "contact", self.username, "version", "1.0.0", "vendor", "myclient")
        mail._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))


if __name__ == "__main__":
    client = NeteaseEmailClient(username=os.getenv('USERNAME'),
                         password=os.getenv('PASSWORD'),
                         email_host=os.getenv('EMAIL_HOST'))
    emails = client.read_emails(criteria="UNSEEN")
    print(json.dumps(emails, ensure_ascii=False))
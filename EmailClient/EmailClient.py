import os
class EmailClient:
    def __init__(self, username: str, password: str, client_type: str):
        self.username = username
        self.password = password
        self.client_type = client_type

    

if __name__ == '__main__':
    client = EmailClient(username=os.getenv('USERNAME'),
                         password=os.getenv('PASSWORD'),
                         client_type=os.getenv('CLIENT_TYPE'))
    print(client)
    print('hello world')
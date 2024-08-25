

import sys

class CCC:
    def byte(self):
        print('=========== bye bye')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.byte()

class AAA(CCC):
    def __init__(self, username) -> None:
        self.username = username
    
    def hello(self):
        print(f'\n\n(AAA)------ hello, {self.username}')

class BBB(CCC):
    def __init__(self, username) -> None:
        self.username = username
    
    def hello(self):
        print(f'\n\n(BBB)------ hello, {self.username}')

class Factory:
    @staticmethod
    def create(username):
        if username == 'tom':
            return AAA(username)
        else:
            return BBB(username)

def test_AAA():
    with Factory.create('tom') as bbb:
        bbb.hello()

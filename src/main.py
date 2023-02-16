from src import FileSystem


class Home:

    def __init__(self):
        self.passwords = {}
        self.groups = {}
        self.users = []

    def login(self):
        username = input("Enter username: ")
        if username == self.passwords[username]:
            self.launch()
        else:
            print()
            print("Wrong username or password")

    def signup(self, username, password):
        self.passwords[username] = password

    def create_group(self, group_name):
        pass

    def launch(self):
        sys = FileSystem()
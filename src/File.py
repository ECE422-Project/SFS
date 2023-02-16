from src.Component import Component
from src.Directory import Directory
from src.User import User

class File(Component):

    def __init__(self, name, directory: Directory, owner: User):
        self.name = name
        self.directory = directory
        self.owner = owner

    def read(self):
        pass

    def write(self):
        pass
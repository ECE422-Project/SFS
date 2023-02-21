from src.Component import Component
from src.Directory import Directory
from src.User import User
import uuid


class File(Component):

    def __init__(self, name, directory: Directory, owner: User):
        self.name = name
        self.directory = directory
        self.owner = owner
        self.uuid = uuid.uuid4()

    def read(self):
        pass

    def write(self):
        pass
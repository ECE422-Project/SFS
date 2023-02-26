from Component import Component
from Directory import Directory
from User import User
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
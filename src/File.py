from Component import Component
from Directory import Directory
from User import User
import uuid


class File(Component):

    def __init__(self, name, directory: Directory, owner: User):
        self.name = name
        self.directory = directory
        self.owner = owner
        self.content = ""

    def read(self):
        return self.content

    def write(self):
        self.content = input("Enter file content: ")

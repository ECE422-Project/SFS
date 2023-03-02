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

    def __eq__(self, other):
        return self.name == other.name and self.directory == other.directory and self.owner == other.owner

    def read(self):
        return self.content

    def write(self, content):
        for word in content:
            if content.index(word) == len(content) - 1:
                self.content += word
            else:
                self.content += word + " "

from Component import Component
from Directory import Directory
from User import User
import uuid
from pyDes import *

class File(Component):

    def __init__(self, name, directory: Directory, owner: User):
        self.name = name
        self.directory = directory
        self.owner = owner
        self.content = ""
        self.last_edited_by = owner.name

    def __eq__(self, other):
        return self.name == other.name and self.directory == other.directory and self.owner == other.owner

    def rename(self, new_name):
        self.name = new_name

    def read(self):
        if self.content == "":
            return ""
        else:
            return triple_des('ECE422-SecurityProject01').decrypt(self.content, padmode=2).decode()
        
    def read_lp(self):
        return self.content

    def write(self, content):
        if self.content != "":
            self.content = triple_des('ECE422-SecurityProject01').decrypt(self.content, padmode=2).decode()
        for word in content:
            if content.index(word) == len(content) - 1:
                self.content += word
            else:
                self.content += word + " "
        self.content = triple_des('ECE422-SecurityProject01').encrypt(self.content, padmode=2)
        self.last_edited_by = self.owner.name

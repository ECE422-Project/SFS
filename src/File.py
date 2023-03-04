from Component import Component
from Directory import Directory
from User import User
from pyDes import *
import hashlib

class File(Component):

    def __init__(self, name, directory: Directory, owner: User):
        self.name = name
        self.directory = directory
        self.owner = owner
        self.content = ""
        self.hash = ""
        self.type = "File"

    def __eq__(self, other):
        return self.name == other.name and self.directory == other.directory and self.owner == other.owner

    # renames the file
    def rename(self, new_name):
        self.name = new_name

    # decrypts and returns the contents of the file
    def read(self):
        if self.content == "":
            return ""
        else:
            return triple_des('ECE422-SecurityProject01').decrypt(self.content, padmode=2).decode()
        
    # returns the still encrypted contents of the file    
    def read_lp(self):
        return self.content

    # adds the encrypted contents to the existing file 
    def write(self, content):
        if self.content != "":
            self.content = triple_des('ECE422-SecurityProject01').decrypt(self.content, padmode=2).decode()
        for word in content:
            if content.index(word) == len(content) - 1:
                self.content += word
            else:
                self.content += word + " "
        self.content = triple_des('ECE422-SecurityProject01').encrypt(self.content, padmode=2)

        # add the encrypted form of the SHA256 hash
        self.hash = hashlib.sha256(self.content).hexdigest()
        self.hash = triple_des('ECE422-SecurityProject01').encrypt(self.hash, padmode=2)
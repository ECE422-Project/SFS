from Component import Component
from User import User
from pyDes import *
import hashlib

class Directory(Component):

    def __init__(self, name, owner: User):
        self.name = name
        self.owner = owner
        self.components = []
        self.hash = ""
        self.type = "Directory"

    def rename(self, new_name):
        self.name = new_name

    def get_files(self):
        return self.components

    def add_component(self, component: Component):
        self.components.append(component)

    def set_owner(self, owner):
        self.owner = owner

    def show_files(self):
        for file in self.components:
            print(file)

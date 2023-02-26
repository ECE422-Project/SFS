from Component import Component
from User import User


class Directory(Component):

    def __init__(self, name, root, owner: User):
        self.name = name
        self.root = root
        self.owner = owner
        self.components = []

    def get_files(self):
        return self.components

    def add_component(self, component: Component):
        self.components.append(component)

    def set_owner(self, owner):
        self.owner = owner

    def show_files(self):
        for file in self.components:
            print(file)

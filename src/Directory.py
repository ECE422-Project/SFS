import Component
import File

class Directory(Component):

    def __init__(self, name, root, owner):
        self.name = name
        self.root = root
        self.owner = owner
        self.files = []

    def get_files(self):
        return self.files

    def add_file(self, file: File):
        self.files.append(file)

    def set_owner(self, owner):
        self.owner = owner

    def show_files(self):
        for file in self.files:
            print(file)

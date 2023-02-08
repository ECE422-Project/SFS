import Component
import Directory
import User

class File(Component):

    def __init__(self, name, directory: Directory, owner: User):
        self.name = name
        self.directory
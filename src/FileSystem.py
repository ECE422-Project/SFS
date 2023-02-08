from enum import Enum
from src.ComponentType import ComponentType
from src.Directory import Directory
from src.File import File


class FileSystem:

    def __init__(self, root: Directory, user):
        self.root = root # the root directory
        self.user = user # the user that is currently logged in
        self.path = [root.name]
        self.pwd = [root]  # list that keeps track of the current working directory and the immediate previous
        # directory
        self.directory_list = {} # dictionary that keeps track of all the directories

    '''
    Return the list containing the string form of the current path
    '''

    def get_current_path(self):
        return self.path

    '''
    Utility function to print the string form of the current path
    '''

    def print_current_path(self):
        print(*self.path)

    '''
    Return the Directory object of the current working directory
    '''

    def get_pwd(self):
        return self.pwd[-1]

    def change_directory(self, directory_name: str):
        self.path.append(directory_name)
        self.pwd.append(self.directory_list[directory_name])


    def change_prev_directory(self):
        self.path.pop()
        self.pwd = self.pop()

    '''
    Creates a new component (so either a file or directory) and then adds it to the dictionary that
    keeps track of what is containing in various directories
    -- We can change this later if structuring things like this gets confusing
    '''

    def create_component(self, name, compType: ComponentType, user):
        # if the component type is a directory, then we add it as an empty list in the dictionary
        if compType == ComponentType.FILE:
            file = File(name, self.get_pwd(), self.user)
            self.get_pwd().add_component(file)
        else:
            directory = Directory(name, self.get_pwd(), self.user)
            self.get_pwd().add_component(directory)
            self.directory_list[name] = directory

from enum import Enum
import ComponentType
import Directory
import File

class FileSystem:

    def __init__(self, directory: Directory, user):
        self.directory = directory
        self.user = user
        self.path = [directory.name]
        self.pwd = [directory]
        self.files = {}

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
        return self.pwd

    '''
    Creates a new component (so either a file or directory) and then adds it to the dictionary that
    keeps track of what is containing in various directories
    -- We can change this later if structuring things like this gets confusing
    '''
    def create_component(self, name, compType: ComponentType.ComponentType):
        # if the component type is a directory, then we add it as an empty list in the dictionary
        if (compType.File):
            file = File(name, self.get_pwd(), self.user)
            self.get_pwd().add_file(file)
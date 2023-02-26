from ComponentType import ComponentType
from Directory import Directory
from File import File
from User import User


class FileSystem:

    def __init__(self):
        self.user = None  # the user that is currently logged in
        self.path = ["/"]
        self.pwd = []  # list that keeps track of the current working directory and the immediate previous
        # directory
        self.directory_list = {}  # dictionary that keeps track of all the directories

    '''
    Return the list containing the string form of the current path
    '''

    def create_user(self, name):
        self.user = User(name)

    def make_current_user(self, user):
        self.user = user

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
        # update the path to the new directory, still needs work
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
    def list_components(self):
        for component in self.get_pwd().get_files():
            print(component.name)

    def create_component(self, name, compType: ComponentType, user):
        # if the component type is a file, then create a new file object and add it to the current directory's list of
        # components
        if compType == ComponentType.FILE:
            file = File(name, self.get_pwd(), self.user)
            self.get_pwd().add_component(file)
        # if the component type is a directory, then create a new directory object and add it to the current directory's
        # list of components and also add it to the dictionary that keeps track of all the directories
        else:
            directory = Directory(name, self.get_pwd(), self.user)
            self.get_pwd().add_component(directory)
            self.directory_list[name] = directory

    def get_component(self, name):
        if name in self.directory_list:
            return self.directory_list[name]
        elif name in self.get_pwd().get_files():
            return self.get_pwd().get_files().index(name)

    def get_groups(self):
        return self.user.groups

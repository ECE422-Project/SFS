from ComponentType import ComponentType
from Directory import Directory
from File import File
from User import User
from AccessRight import PermissionType
from pyDes import *

class FileSystem:

    def __init__(self, client):
        self.user = None  # the user that is currently logged in
        self.users = []  # list of all the users
        self.path = ["/"]
        self.pwd = []  # list that keeps track of the current working directory and the immediate previous
        # directory
        self.directory_list = {}  # dictionary that keeps track of all the directories
        self.pwd.append(Directory("/", self.user))

    '''
    Return the list containing the string form of the current path
    '''

    def create_user(self, name):
        self.user = User(name)
        self.users.append(self.user)

    def make_current_user(self, name):
        for user in self.users:
            if user.name == name:
                self.user = user
                directory = self.create_component(self.user.home_directory, ComponentType.DIR)
                self.change_directory(self.user.home_directory)
                print(self.directory_list)
                return
        self.create_user(name)
        self.make_current_user(name)

    '''
    Return the list containing the string form of the current path
    '''

    def get_current_path(self):
        decryptedPath = ["/"]
        for i in range(1, len(self.path)):
            decryptedPath.append(triple_des('ECE422-SecurityProject01').decrypt(self.path[i], padmode=2).decode())
        return decryptedPath
    
    # returns the still encrypted current directory path
    def get_current_path_lp(self):
        return self.path

    '''
    Return the Directory object of the current working directory
    '''

    def get_pwd(self):
        print(isinstance(self.pwd, list))
        return self.pwd[len(self.pwd) - 1]

    def change_directory(self, directory_name: str):
        directory_name = triple_des('ECE422-SecurityProject01').encrypt(directory_name, padmode=2)
        # update the path to the new directory, still needs work
        self.path.append(directory_name)
        try:
            self.pwd.append(self.directory_list[directory_name])
            return True
        except:
            return False

    def change_prev_directory(self):
        self.path.pop()
        self.pwd.pop()

    '''
    Creates a new component (so either a file or directory) and then adds it to the dictionary that
    keeps track of what is containing in various directories
    -- We can change this later if structuring things like this gets confusing
    '''

    def list_components(self):
        li = []
        for component in self.get_pwd().get_files():
            li.append(triple_des('ECE422-SecurityProject01').decrypt(component.name, padmode=2).decode())
        return li
    
    # returns the still encrypted list of all files and directories
    def list_components_lp(self):
        li = []
        for component in self.get_pwd().get_files():
            li.append(component.name)
        return li

    # creates a new file or directory
    def create_component(self, name, compType: ComponentType):
        # use encrypted form of the component name 
        name = triple_des('ECE422-SecurityProject01').encrypt(name, padmode=2)
        # if the component type is a file, then create a new file object and add it to the current directory's list of
        # components
        if compType == ComponentType.FILE:
            file = File(name, self.get_pwd(), self.user)
            self.get_pwd().add_component(file)
            self.user.permissions[file.name] = PermissionType.READWRITE
            return file
        # if the component type is a directory, then create a new directory object and add it to the current directory's
        # list of components and also add it to the dictionary that keeps track of all the directories
        else:
            directory = Directory(name, self.get_pwd())
            self.get_pwd().add_component(directory)
            self.directory_list[name] = directory
            self.user.permissions[directory.name] = PermissionType.READWRITE
            return directory

    # deletes a file or directory
    def remove_component(self, name):
        # use encrypted form of the component name 
        name = triple_des('ECE422-SecurityProject01').encrypt(name, padmode=2)
        if name in self.directory_list:
            self.directory_list.pop(name)
        else:
            for directory in self.directory_list:
                for file in self.directory_list[directory].get_files():
                    if name in file.name:
                        self.directory_list[directory].get_files().remove(file)

    # retrives a file or directory
    def get_component(self, name):
        # use encrypted form of the component name 
        name = triple_des('ECE422-SecurityProject01').encrypt(name, padmode=2)
        if name in self.directory_list:
            return self.directory_list[name]
        else:
            for directory in self.directory_list:
                for file in self.directory_list[directory].get_files():
                    if name in file.name:
                        return file

    # returns the list of all groups assigned to a user
    def get_groups(self):
        return self.user.groups

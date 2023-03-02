from ComponentType import ComponentType
from Directory import Directory
from File import File
from User import User


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
                self.create_component(self.user.home_directory, ComponentType.DIR)
                self.change_directory(self.user.home_directory)
                return
        self.create_user(name)
        self.make_current_user(name)

    '''
    Return the list containing the string form of the current path
    '''

    def get_current_path(self):
        return self.path

    '''
    Return the Directory object of the current working directory
    '''

    def get_pwd(self):
        return self.pwd[len(self.pwd) - 1]

    def change_directory(self, directory_name: str):
        # update the path to the new directory, still needs work
        self.path.append(directory_name)
        self.pwd.append(self.directory_list[directory_name])

    def change_prev_directory(self):
        self.path.pop()
        self.pwd = self.pwd.pop()

    '''
    Creates a new component (so either a file or directory) and then adds it to the dictionary that
    keeps track of what is containing in various directories
    -- We can change this later if structuring things like this gets confusing
    '''

    def list_components(self):
        li = []
        for component in self.get_pwd().get_files():
            li.append(component.name)
        return li

    def create_component(self, name, compType: ComponentType):
        # if the component type is a file, then create a new file object and add it to the current directory's list of
        # components
        if compType == ComponentType.FILE:
            file = File(name, self.get_pwd(), self.user)
            self.get_pwd().add_component(file)
            return file
        # if the component type is a directory, then create a new directory object and add it to the current directory's
        # list of components and also add it to the dictionary that keeps track of all the directories
        else:
            directory = Directory(name, self.get_pwd())
            self.get_pwd().add_component(directory)
            self.directory_list[name] = directory
            return directory

    def remove_component(self, name):
        if name in self.directory_list:
            self.directory_list.pop(name)
        elif name in self.get_pwd().get_files():
            self.get_pwd().get_files().remove(name)

    def rename_component(self, old_name, new_name):
        if old_name in self.directory_list:
            self.directory_list[new_name] = self.directory_list.pop(old_name)
        elif old_name in self.get_pwd().get_files():
            self.get_pwd().get_files().remove(old_name)
            self.get_pwd().get_files().append(new_name)

    def get_component(self, name):
        if name in self.directory_list:
            return self.directory_list[name]
        elif name in self.get_pwd().get_files():
            for file in self.get_pwd().get_files():
                if file.name == name:
                    return file

    def get_groups(self):
        return self.user.groups

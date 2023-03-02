class User:

    def __init__(self, name):
        self.name = name
        self.groups = []
        self.permissions = {}
        self.home_directory = "home/" + name

    def add_group(self, group):
        if group not in self.groups:
            self.groups.append(group)
        else:
            pass

    def remove_group(self, group):
        self.groups.remove(group)

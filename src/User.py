from src import Component


class User:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.groups = []
        self.permissions = {}

    def add_group(self, group):
        self.groups.append(group)

    def remove_group(self, group):
        self.groups.remove(group)

    def add_permission(self, component: Component, permission):
        self.permissions[component] = permission


from src import User


class Component:

    def __init__(self, name, owner: User):
        self.name = name
        self.owner = owner

    def set_owner(self, owner):
        self.owner = owner

    def set_permission(self, user, permission
        user.add_permission(self, permission)

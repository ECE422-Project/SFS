from src import User
from src import AccessRight


class Component:

    def __init__(self, name, owner: User):
        self.name = name
        self.owner = owner

    def set_owner(self, owner):
        self.owner = owner

    def get_owner(self):
        return self.owner

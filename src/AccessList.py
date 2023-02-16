from src import AccessRight
from src.AccessRight import *


class AccessList:
    def __init__(self):
        self.accessMap = {}

    def add_access(self, username: str, access: AccessRight):
        if self.accessMap.__contains__(username):
            self.accessMap[username].append(access)
        else:
            self.accessMap[username] = [access]

    def check_access(self, username: str, component: str, permission: PermissionType):
        access = AccessRight(component, permission)
        return self.accessMap.__contains__(username) and self.accessMap[username].__contains__(access)

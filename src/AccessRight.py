class PermissionType:
    NONE = 0
    READ = 1
    WRITE = 2
    READWRITE = 3


class AccessRight:

    def __init__(self, component: str, permission: PermissionType):
        self.component = component
        self.permission = permission

    def __eq__(self, other):
        return self.component == other.component and self.permission == other.permission

    def get_user(self):
        return self.component

    def get_permission(self):
        return self.permission

    def set_permission(self, permission):
        self.permission = permission

    def set_user(self, component):
        self.component = component

    def __str__(self):
        return "User: " + self.component + " Permission: " + str(self.permission)




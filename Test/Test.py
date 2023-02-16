import unittest
from src.FileSystem import FileSystem
from src.Directory import Directory
from src.User import User
from src.ComponentType import ComponentType
from src.AccessRight import *
from src.AccessList import AccessList



class MyTestCase(unittest.TestCase):
    def test_file_system(self):
        user = User("User 1")
        root = Directory(name="/", root=None, owner=user)   # root directory
        sys = FileSystem(root=root, user=user)
        sys.create_component("home", ComponentType.DIR, user)
        sys.change_directory("home")

        self.assertEqual(sys.get_pwd().name, "home")  # add assertion here

    def test_permissions(self):
        user = User("User 1")
        user2 = User("User 2")
        root = Directory(name="/", root=None, owner=user)  # root directory
        sys = FileSystem(root=root, user=user)
        sys.create_component("home", ComponentType.DIR, user)
        access_list = AccessList()
        access_list.add_access(user.name, AccessRight("home", PermissionType.READWRITE))
        self.assertEqual(
            True,
            access_list.check_access(user.name, "home", PermissionType.READWRITE)
        )
        self.assertEqual(
            False,
            access_list.check_access(user2.name, "home", PermissionType.READWRITE)
        )



if __name__ == '__main__':
    unittest.main()

import unittest
from src.FileSystem import FileSystem
from src.Directory import Directory
from src.User import User
from src.ComponentType import ComponentType



class MyTestCase(unittest.TestCase):
    def test_file_system(self):
        user = User("User 1")
        root = Directory(name="/", root=None, owner=user)   # root directory
        sys = FileSystem(root=root, user=user)
        sys.create_component("home", ComponentType.DIR, user)
        sys.change_directory("home")

        self.assertEqual(sys.get_pwd().name, "home")  # add assertion here


if __name__ == '__main__':
    unittest.main()

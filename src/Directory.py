
class Directory:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.files = []


    def getFiles(self):
        return self.files

    def addFile(self, file):
        self.files.append(file)

    def setOwner(self, owner):
        self.owner = owner

    def showFiles(self):
        for file in self.files:
            print(file)
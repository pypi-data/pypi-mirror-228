class File():

    """
    Speeds up interaction with files.
    """

    def __init__(self, path=None, data=None):

        self.path = path
        self.data = data

    def readlines(self):

        try:
            f = open(f'{self.path}')
            raw = f.readlines()
            f.close()
            return raw

        except FileNotFoundError:
            print("Something went wrong.")

    def readline(self):

        try:
            f = open(f'{self.path}')
            raw = f.readline()
            f.close()
            return raw

        except FileNotFoundError:
            print("Something went wrong.")

    def read(self):

        try:
            f = open(f'{self.path}')
            raw = f.read()
            f.close()
            return raw

        except FileNotFoundError:
            print("Something went wrong.")

    def write(self):

        try:
            file = open(f"{self.path}", "w")
            file.write(f"{self.data}")
            file.close()

        except FileNotFoundError:
            print("Something went wrong.")

    def add(self):

        try:
            file = open(f"{self.path}", "a")
            file.write(f"{self.data}")
            file.close()

        except FileNotFoundError:
            print("Something went wrong.")
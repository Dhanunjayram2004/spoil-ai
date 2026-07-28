import os


class Session:

    def __init__(self):

        self.cwd = os.getcwd()

    def pwd(self):

        return self.cwd

    def cd(self, path):

        path = os.path.abspath(
            os.path.join(self.cwd, path)
        )

        if not os.path.isdir(path):

            return False

        self.cwd = path

        os.chdir(path)

        return True

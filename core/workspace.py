from pathlib import Path


class Workspace:

    def write(self, cwd, filename, content):

        path = Path(cwd) / filename

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content)

        return path

    def read(self, cwd, filename):

        path = Path(cwd) / filename

        return path.read_text()

    def exists(self, cwd, filename):

        return (Path(cwd) / filename).exists()

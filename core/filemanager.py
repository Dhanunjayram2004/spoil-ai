from pathlib import Path


class FileManager:

    def read(self, filename):

        path = Path(filename)

        if not path.exists():
            return None

        return path.read_text()

    def write(self, filename, content):

        path = Path(filename)

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content)

        return str(path)

    def exists(self, filename):

        return Path(filename).exists()

    def list(self, directory="."):

        return [str(p) for p in Path(directory).iterdir()]

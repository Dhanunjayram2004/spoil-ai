import os
import subprocess


class Shell:

    def execute(self, command):

        command = command.strip()

        if not command:
            return ""

        # cd must be handled by us because it's a shell builtin
        if command.startswith("cd"):

            parts = command.split(maxsplit=1)

            if len(parts) == 1:
                path = os.path.expanduser("~")
            else:
                path = os.path.expanduser(parts[1])

            try:
                os.chdir(path)
                return ""
            except Exception as e:
                return str(e)

        # Run everything else exactly like a Linux terminal
        process = subprocess.Popen(
            command,
            shell=True
        )

        process.wait()

        return ""

from core.llm import LLM
from core.planner import Planner
from core.dependency import check_command, install_package
import subprocess
from core.privilege import needs_sudo

class Agent:

    def __init__(self):

        self.planner = Planner()
        self.chatbot = LLM()

    def run_command(self, command):

        print(f"\n$ {command}\n")

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        output = ""

        try:

            for line in process.stdout:
                print(line, end="")
                output += line

            process.wait()

        except KeyboardInterrupt:

            process.kill()
            print("\nInterrupted.")

        return ""

    def ensure_packages(self, packages):

        for package in packages:

            if check_command(package):
                continue

            print(f"\nSPOIL needs '{package}'")
            print(f"sudo apt install {package} -y\n")

            if not install_package(package):
                return False

        return True

    def chat(self, user):

        plan = self.planner.plan(user)


        if plan["action"] == "chat":

            return plan["message"]

        if plan["action"] == "run":

            if not self.ensure_packages(plan["packages"]):
                return "Cancelled."


            for command in plan["commands"]:
                command = command.strip()
                while command.startswith("sudo "):
                    command = command[5:].strip()
                if needs_sudo(command):
                   answer = input(f"\n'{command}' requires administrator privileges.\nRun with sudo (y/n):").strip().lower()
                   if answer != "y":
                      continue
                   command = "sudo " + command

                self.run_command(command)
            return ""

        return ""




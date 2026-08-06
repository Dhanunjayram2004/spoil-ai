from core.llm import LLM
from core.planner import Planner
from core.dependency import check_command, install_package
from core.privilege import needs_sudo
from core.executor import Executor
import subprocess

class Agent:
    def __init__(self):
        self.planner = Planner()
        self.chatbot = LLM()
        self.executor = Executor()

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
        return output

    def ensure_packages(self, packages):
        for package in packages:
            if check_command(package):
                continue
            if not install_package(package):
                return False
        return True

    def chat(self, user):
        # 1. Planner dynamically decides what to do
        plan = self.planner.plan(user)

        # 2. If it's chat, trigger the direct streaming LLM!
        if plan.get("action") == "chat":
            print()
            self.chatbot.chat([{"role": "user", "content": user}], stream=True)
            print()
            return ""

        # 3. Tool Execution
        if plan.get("action") == "tool":
            if plan["tool"] == "network_scan":
                network = self.executor.execute("get_network_range")
                if not network["success"]:
                    return network.get("stderr", network.get("error", "Unknown Error"))
                result = self.executor.execute("network_scan", network=network["stdout"])
            else:
                result = self.executor.execute(plan["tool"])

            if result.get("stdout"):
                print(result["stdout"])
            if result.get("stderr"):
                print(result["stderr"])
            if result.get("error"):
                print(f"Tool Error: {result['error']}")
            return ""

        # 4. Command Execution
        if plan.get("action") == "run":
            if not self.ensure_packages(plan.get("packages", [])):
                return "Cancelled."

            for command in plan.get("commands", []):
                command = command.strip()
                while command.startswith("sudo "):
                    command = command[5:].strip()

                if needs_sudo(command):
                    answer = input(
                        f"\n'{command}' requires administrator privileges.\nRun with sudo (y/n): "
                    ).strip().lower()
                    if answer != "y":
                        continue
                    command = "sudo " + command

                self.run_command(command)
            return ""

        return ""

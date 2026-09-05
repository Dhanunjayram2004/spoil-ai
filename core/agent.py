import json
import re
import subprocess
import time
from core.llm import LLM
from core.registry import list_tools
from core.executor import Executor
from core.dependency import check_command, install_package
from core.privilege import needs_sudo
from core.tool_schema import get_tool_schema
from core.memory import MemoryManager
from pathlib import Path
SHELL_TOOL_NAME = "run_shell_command"


def shell_tool_schema():
    return {
        "type": "function",
        "function": {
            "name": SHELL_TOOL_NAME,
            "description": (
                "Run Linux shell command(s) to accomplish a request that no other "
                "registered tool covers. Use for diagnostics, info-gathering, or "
                "any ad-hoc task requiring real commands."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Shell commands to run in order. No sudo prefix.",
                    },
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "APT package names required by the commands, if any.",
                    },
                },
                "required": ["commands"],
            },
        },
    }


class Agent:
    def __init__(self):
        self.llm = LLM()
        self.executor = Executor()
        self.memory = MemoryManager()

    def run_command(self, command):
        print(f"\n$ {command}\n")
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1,
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
            
        if output and not output.endswith("\n"):
            print()
        return output
    def find_target_directory(self, query: str):
        match = re.search(r'\b(go to|cd to|switch to|navigate to|open|move to|change to)\s+([a-zA-Z0-9_\-\./]+)', query.lower())
        if not match:
            return None
            
        target_name = match.group(2).strip('/')
        current_dir = Path.cwd().resolve()
        
        # 1. Direct relative path check (e.g. "go to ..", "go to ../..")
        direct_path = (current_dir / target_name).resolve()
        if direct_path.is_dir():
            return str(direct_path)

        # 2. Search upward in Parent Hierarchy (Fix for going back to parent/sibling folders like /opt/spoil)
        for parent in [current_dir] + list(current_dir.parents):
            if parent.name.lower() == target_name.lower():
                return str(parent)
            if parent != Path('/'):
                for child in parent.iterdir():
                    if child.is_dir() and child.name.lower() == target_name.lower():
                        return str(child)

        # 3. Search downward in Home directory tree
        try:
            for path in Path.home().rglob(target_name):
                if path.is_dir():
                    return str(path.resolve())
        except Exception:
            pass
                
        return None
    def ensure_packages(self, packages):
        for package in packages or []:
            print(f"[DEBUG] checking package: {package}")
            t0 = time.time()
            have_it = check_command(package)
            print(f"[DEBUG] check_command({package}) = {have_it} ({time.time()-t0:.2f}s)")
            if have_it:
                continue
            answer = input(f"\nPackage '{package}' is missing. Do you want to install it? (y/n): ").strip().lower()
            if answer != "y":
                print(f"Skipping installation of '{package}'.")
                return False
            print(f"[DEBUG] installing package: {package}")
            t0 = time.time()
            ok = install_package(package)
            print(f"[DEBUG] install_package({package}) = {ok} ({time.time()-t0:.2f}s)")
            if not ok:
                return False
        return True

    def dispatch_tool_call(self, call):
        print(f"[DEBUG] tool={call.function.name} args={call.function.arguments}")
        name = call.function.name
        try:
            args = json.loads(call.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}

        if name == SHELL_TOOL_NAME:
            if not self.ensure_packages(args.get("packages", [])):
                print("Cancelled: missing dependency.")
                return
            for command in args.get("commands", []):
                command = command.strip()
                while command.startswith("sudo "):
                    command = command[5:].strip()
                if needs_sudo(command):
                    answer = input(f"\n'{command}' needs sudo. Run with sudo (y/n): ").strip().lower()
                    if answer != "y":
                        continue
                    command = "sudo " + command
                self.run_command(command)
            return

        result = self.executor.execute(name, **args)
        if result.get("stdout"):
            print(result["stdout"])
        if result.get("stderr"):
            print(result["stderr"])
        if result.get("error"):
            print(f"Tool Error: {result['error']}")

    def chat(self, user):
        target_dir = self.find_target_directory(user)
        if target_dir:
            print(f"__CHDIR__:{target_dir}")
            return ""
        tools = get_tool_schema() + [shell_tool_schema()]

        # 1. Retrieve RAG Context dynamically for the query
        rag_context = self.memory.retrieve_rag_context(user)

        # 2. Build the messages payload
        messages = []
        if rag_context:
            messages.append({
                "role": "system",
                "content": f"Relevant workspace context:\n{rag_context}\nUse this context to inform your commands and answers."
            })
        messages.append({"role": "user", "content": user})

        # 3. Pass augmented messages to LLM
        t0 = time.time()
        message = self.llm.chat(
            messages,
            tools=tools,
            tool_choice="auto",
            stream=False,
        )
        print(f"[DEBUG] llm.chat took {time.time()-t0:.2f}s")

        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                t0 = time.time()
                self.dispatch_tool_call(call)
                print(f"[DEBUG] dispatch_tool_call took {time.time()-t0:.2f}s")
            return ""

        if message.content:
            match = re.search(r'\{[^{}]*"commands"\s*:\s*\[.*?\][^{}]*\}', message.content, re.DOTALL)
            if match:
                try:
                    args = json.loads(match.group(0))
                    for command in args.get("commands", []):
                        self.run_command(command.strip())
                    return ""
                except json.JSONDecodeError:
                    pass
            print(message.content)
        return ""

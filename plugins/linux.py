import subprocess
from core.registry import tool


@tool(
    name="linux_command",
    description="Run Linux terminal commands"
)
def linux_command(command):

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

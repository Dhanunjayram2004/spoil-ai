import subprocess

from core.registry import tool


@tool(
    name="run_command",
    description="Execute a Linux shell command and return stdout, stderr and exit code."
)
def run_command(command: str):
    """
    Execute a shell command.
    """

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

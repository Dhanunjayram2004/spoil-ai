import subprocess


class Runner:

    def run_python(self, filename):

        try:
            result = subprocess.run(
                ["python3", filename],
                capture_output=True,
                text=True,
                timeout=30,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Program timed out after 30 seconds.",
                "returncode": -1,
            }

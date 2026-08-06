from core.registry import get_tool
from core.dependency import check_command, install_package


class Executor:

    def execute(self, tool_name, **kwargs):

        tool = get_tool(tool_name)

        if tool is None:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        # Generic dependency handling
        if getattr(tool, "requires", None):

            if not check_command(tool.requires):

                print(f"\nSPOIL needs '{tool.requires}'")

                if not install_package(tool.requires):
                    return {
                        "success": False,
                        "stderr": "Installation cancelled."
                    }

        try:
            return tool.function(**kwargs)

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

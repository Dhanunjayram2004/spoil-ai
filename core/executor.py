from core.registry import get_tool


class Executor:

    def execute(self, tool_name, **kwargs):

        tool = get_tool(tool_name)

        if tool is None:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        try:
            return tool.function(**kwargs)

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

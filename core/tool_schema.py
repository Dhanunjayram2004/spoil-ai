from core.registry import list_tools


def get_tool_schema():

    schemas = []

    for name, tool in list_tools().items():

        schemas.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Input for the tool"
                            }
                        },
                        "required": []
                    }
                }
            }
        )

    return schemas

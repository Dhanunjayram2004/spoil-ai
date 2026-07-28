import inspect
from core.registry import list_tools


TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}


def ollama_tools():
    tools = []

    for name, func in list_tools().items():

        sig = inspect.signature(func)

        properties = {}
        required = []

        for param in sig.parameters.values():

            json_type = TYPE_MAP.get(param.annotation, "string")

            properties[param.name] = {
                "type": json_type
            }

            if param.default is inspect._empty:
                required.append(param.name)

        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": func.__doc__ or "",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        })

    return tools

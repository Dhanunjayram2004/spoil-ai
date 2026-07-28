"""
SPOIL Tool Registry

Every tool registers itself automatically using @tool.

Supports:
- tool name
- description
- required Linux package dependency
"""

TOOLS = {}



class Tool:

    def __init__(
        self,
        name,
        description,
        function,
        requires=None
    ):

        self.name = name
        self.description = description
        self.function = function
        self.requires = requires



def tool(
    name,
    description,
    requires=None
):
    """
    Decorator used by plugins to register tools.

    Example:

    @tool(
        "network_scan",
        "Scan local network",
        requires="nmap"
    )
    """

    def decorator(func):

        TOOLS[name] = Tool(
            name=name,
            description=description,
            function=func,
            requires=requires
        )

        return func


    return decorator



def get_tool(name):

    return TOOLS.get(name)



def list_tools():

    return TOOLS

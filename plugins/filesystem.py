from pathlib import Path

from core.registry import tool


@tool(
    name="write_file",
    description="Create or overwrite a text file."
)
def write_file(path: str, content: str):

    file = Path(path)

    file.parent.mkdir(parents=True, exist_ok=True)

    file.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "message": f"Wrote {path}"
    }


@tool(
    name="read_file",
    description="Read a text file."
)
def read_file(path: str):

    file = Path(path)

    if not file.exists():
        return {
            "success": False,
            "error": "File does not exist."
        }

    return {
        "success": True,
        "content": file.read_text(encoding="utf-8")
    }


@tool(
    name="list_directory",
    description="List files inside a directory."
)
def list_directory(path: str = "."):

    directory = Path(path)

    if not directory.exists():
        return {
            "success": False,
            "error": "Directory not found."
        }

    return {
        "success": True,
        "items": sorted([p.name for p in directory.iterdir()])
    }

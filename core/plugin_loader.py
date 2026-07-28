"""
Ghost Plugin Loader

Automatically imports every plugin inside the plugins directory.
"""

import importlib
from pathlib import Path


def load_plugins():

    plugins_dir = Path(__file__).parent.parent / "plugins"

    for file in plugins_dir.glob("*.py"):

        if file.name.startswith("_"):
            continue

        module = f"plugins.{file.stem}"

        importlib.import_module(module)

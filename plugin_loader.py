"""
plugin_loader.py
Version: 1.0
Summary: Dynamically loads all modules in specified plugin packages so that any decorators
         (and hence plugin registrations) are executed.
"""

import importlib
import pkgutil
from typing import List

def load_plugins_from_package(package_name: str) -> None:
    """
    Dynamically imports all modules in the given package so that any decorators are executed.

    Parameters:
        package_name (str): The dot-separated name of the package to load plugins from.
    """
    package = importlib.import_module(package_name)
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        importlib.import_module(module_name)

def load_all_plugins(packages: List[str]) -> None:
    """
    Loads plugins from all packages listed.

    Parameters:
        packages (List[str]): A list of dot-separated package names to load plugins from.
    """
    for package_name in packages:
        load_plugins_from_package(package_name)
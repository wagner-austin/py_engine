"""
plugin_loader.py
Version: 1.0 (Updated with debug print statements)

Summary: Dynamically loads all modules in specified plugin packages so that any decorators
         (and hence plugin registrations) are executed. Now prints out debug info for each
         package and module loaded.
"""

import importlib
import pkgutil
from typing import List

def load_plugins_from_package(package_name: str) -> None:
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        print(f"[Plugin Loader] Error importing package '{package_name}': {e}")
        return

    print(f"[Plugin Loader] Loaded package '{package_name}' with path: {package.__path__}")
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            print(f"[Plugin Loader] Importing module: {module_name}")
            importlib.import_module(module_name)
        except Exception as e:
            print(f"[Plugin Loader] Error importing module '{module_name}': {e}")

def load_all_plugins(packages: List[str]) -> None:
    for package_name in packages:
        print(f"[Plugin Loader] Loading plugins from package: {package_name}")
        load_plugins_from_package(package_name)
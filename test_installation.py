#!/usr/bin/env python3
"""
Test script for XShot installation.

This script verifies that the XShot package can be imported correctly.
"""

import sys
import os
import importlib

def test_imports():
    """Test importing XShot modules."""
    modules = [
        "xshot_py",
        "xshot_py.core.app",
        "xshot_py.config.config_manager",
        "xshot_py.themes.theme_manager",
        "xshot_py.core.image_processor",
        "xshot_py.core.file_watcher",
        "xshot_py.ui.app_ui",
        "xshot_py.ui.base_ui",
    ]
    
    success = True
    for module_name in modules:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ Successfully imported {module_name}")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {e}")
            success = False
    
    return success

def test_package_structure():
    """Test the package structure."""
    import xshot_py
    
    # Get the package directory
    package_dir = os.path.dirname(xshot_py.__file__)
    print(f"Package directory: {package_dir}")
    
    # Check for required directories
    required_dirs = ["core", "config", "themes", "ui", "assets"]
    success = True
    
    for directory in required_dirs:
        dir_path = os.path.join(package_dir, directory)
        if os.path.isdir(dir_path):
            print(f"✅ Found directory: {directory}")
        else:
            print(f"❌ Missing directory: {directory}")
            success = False
    
    return success

def main():
    """Run the tests."""
    print("Testing XShot installation...")
    print("\nTesting imports:")
    imports_ok = test_imports()
    
    print("\nTesting package structure:")
    structure_ok = test_package_structure()
    
    if imports_ok and structure_ok:
        print("\n✅ All tests passed! XShot is installed correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
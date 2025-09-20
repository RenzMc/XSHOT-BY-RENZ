#!/usr/bin/env python3
"""
Setup Assets for XShot

This script copies required assets from the original XShot project.
"""

import os
import shutil
from pathlib import Path

def setup_fonts(source_dir, target_dir):
    """
    Copy fonts from source directory to target directory.
    
    Args:
        source_dir: Source directory
        target_dir: Target directory
    """
    print(f"Copying fonts from {source_dir} to {target_dir}")
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy all font files
    for font_file in Path(source_dir).glob("*.ttf"):
        target_file = os.path.join(target_dir, font_file.name)
        shutil.copy2(font_file, target_file)
        print(f"Copied {font_file.name}")

def main():
    """
    Main entry point.
    """
    # Get script directory
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Source directories
    xshot_dir = os.path.join(os.path.dirname(script_dir), "xshot_analysis", "XShot")
    fonts_dir = os.path.join(xshot_dir, "fonts")
    
    # Target directories
    assets_dir = os.path.join(script_dir, "assets")
    target_fonts_dir = os.path.join(assets_dir, "fonts")
    
    # Create assets directory if it doesn't exist
    os.makedirs(assets_dir, exist_ok=True)
    
    # Copy fonts
    setup_fonts(fonts_dir, target_fonts_dir)
    
    print("Assets setup complete!")

if __name__ == "__main__":
    main()
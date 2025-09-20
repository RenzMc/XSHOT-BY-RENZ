#!/usr/bin/env python3
"""
XShot - Screenshot Enhancement Tool

A highly customizable screenshot enhancement tool with a rich UI.
"""

import os
import sys
import argparse
from typing import Dict, Any, List, Optional

def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    required_packages = [
        ('PIL', 'Pillow'),
        ('rich', 'rich'),
        ('watchdog', 'watchdog'),
        ('yaml', 'PyYAML'),
        ('click', 'click'),
        ('dotenv', 'python-dotenv'),
        ('numpy', 'numpy')
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("Error: Missing required dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install missing dependencies using:")
        print(f"  pip install {' '.join(missing_packages)}")
        print("Or run: pip install -r requirements.txt")
        return False
    
    return True

# Check dependencies before importing rich components
if not check_dependencies():
    sys.exit(1)

from rich.console import Console
from rich.traceback import install

# Install rich traceback handler
install(show_locals=True)

# Import modules using absolute imports
from xshot_py.core.app import XShotApp
from xshot_py.config.config_manager import ConfigManager
from xshot_py.themes.theme_manager import ThemeManager
from xshot_py.core.image_processor import ImageProcessor

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="XShot - Screenshot Enhancement Tool")
    
    # Mode arguments
    mode_group = parser.add_argument_group("Mode")
    mode_group.add_argument("-a", "--auto", action="store_true", help="Run in auto screenshot mode")
    mode_group.add_argument("-m", "--manual", action="store_true", help="Run in manual screenshot mode")
    
    # Theme arguments
    theme_group = parser.add_argument_group("Theme")
    theme_group.add_argument("-t", "--theme", help="Set theme (dark, light, nord, dracula, or custom theme ID)")
    
    # Processing arguments
    proc_group = parser.add_argument_group("Processing")
    proc_group.add_argument("-i", "--input", help="Input file to process")
    proc_group.add_argument("-o", "--output", help="Output directory")
    proc_group.add_argument("--no-titlebar", action="store_true", help="Disable titlebar")
    proc_group.add_argument("--no-footer", action="store_true", help="Disable footer")
    proc_group.add_argument("--no-custom-image", action="store_true", help="Disable custom image")
    
    # Configuration arguments
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument("--config", help="Path to config directory")
    config_group.add_argument("--list-themes", action="store_true", help="List available themes")
    
    return parser.parse_args()

def process_single_file(args):
    """
    Process a single file based on command line arguments.
    
    Args:
        args: Command line arguments
    """
    console = Console()
    
    # Initialize configuration
    config_dir = args.config if args.config else None
    config_manager = ConfigManager(config_dir)
    theme_manager = ThemeManager(os.path.join(config_manager.config_dir, "themes"))
    
    # Get configuration safely
    config = config_manager.config
    if config is None:
        console.print("[bold red]Error: Failed to load configuration[/bold red]")
        return
    
    # Override configuration with command line arguments
    if args.theme:
        config_manager.set("appearance", "theme", args.theme)
    
    if args.output:
        config_manager.set("general", "output_dir", args.output)
    
    if args.no_titlebar:
        config_manager.set("titlebar", "enabled", False)
    
    if args.no_footer:
        config_manager.set("footer", "enabled", False)
    
    if args.no_custom_image:
        config_manager.set("custom_image", "enabled", False)
    
    # Get theme data
    theme_id = config_manager.safe_get_nested("appearance.theme", "dark")
    theme_data = theme_manager.get_theme(theme_id)
    
    # Initialize image processor
    image_processor = ImageProcessor(config, theme_data)
    
    # Process the file
    console.print(f"Processing file: {args.input}")
    output_path = image_processor.process_image(args.input)
    console.print(f"Output file: {output_path}")

def list_themes():
    """
    List available themes.
    """
    console = Console()
    
    # Initialize configuration
    config_manager = ConfigManager()
    theme_manager = ThemeManager(os.path.join(config_manager.config_dir, "themes"))
    
    # Get theme list
    themes = theme_manager.get_theme_list()
    
    console.print("[bold]Available Themes:[/bold]")
    for theme in themes:
        console.print(f"[cyan]{theme['id']}[/cyan]: {theme['name']} - {theme['description']} ({theme['type']})")

def main():
    """
    Main entry point.
    """
    args = parse_args()
    
    # Handle special commands
    if args.list_themes:
        list_themes()
        return
    
    # Handle single file processing
    if args.input:
        process_single_file(args)
        return
    
    # Run the application
    app = XShotApp()
    
    if args.auto:
        app.run_auto_mode()
    elif args.manual:
        app.run_manual_mode()
    else:
        app.run()

if __name__ == "__main__":
    main()
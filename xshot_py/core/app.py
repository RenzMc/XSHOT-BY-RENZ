"""
Main Application for XShot

This module provides the main application class for XShot.
"""

import os
import sys
import time
import platform
import subprocess
import shutil
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Use absolute imports instead of relative imports
from xshot_py.config.config_manager import ConfigManager
from xshot_py.themes.theme_manager import ThemeManager
from xshot_py.core.image_processor import ImageProcessor
from xshot_py.core.file_watcher import FileWatcher
from xshot_py.ui.app_ui import AppUI

class XShotApp:
    """
    Main application class for XShot.
    """
    
    def __init__(self):
        """
        Initialize the application.
        """
        # Set up base directories
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_dir = os.path.expanduser("~/.config/xshot")
        self.themes_dir = os.path.join(self.config_dir, "themes")
        
        # Ensure directories exist
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.themes_dir, exist_ok=True)
        
        # Initialize managers
        self.config_manager = ConfigManager(self.config_dir)
        self.theme_manager = ThemeManager(self.themes_dir)
        
        # Load configuration
        self.config = self.config_manager.config
        
        # Get current theme
        theme_id = self.config["appearance"]["theme"]
        self.theme_data = self.theme_manager.get_theme(theme_id)
        
        # Initialize UI
        self.ui = AppUI(self.config_manager, self.theme_manager)
        
        # Initialize image processor
        self.image_processor = ImageProcessor(self.config, self.theme_data)
        
        # Initialize file watcher
        self.file_watcher = FileWatcher(self.config["auto_detection"], self.process_new_screenshot)
    
    def run(self):
        """
        Run the application.
        """
        try:
            while True:
                # Show main menu
                choice = self.ui.show_main_menu()
                
                if choice == "1":  # Auto Screenshot Mode
                    self.run_auto_mode()
                elif choice == "2":  # Manual Screenshot Mode
                    self.run_manual_mode()
                elif choice == "3":  # Settings
                    self.run_settings()
                elif choice == "4":  # Themes
                    self.run_themes()
                elif choice == "5":  # Help
                    self.ui.show_help()
                elif choice == "q":  # Quit
                    break
        except KeyboardInterrupt:
            pass
        finally:
            # Clean up
            if self.file_watcher.is_running():
                self.file_watcher.stop()
            
            self.ui.clear()
            self.ui.print("[bold green]Thank you for using XShot![/bold green]")
    
    def run_auto_mode(self):
        """
        Run auto screenshot mode.
        """
        # Check if auto detection is enabled
        if not self.config["auto_detection"]["enabled"]:
            self.ui.print("[bold yellow]Auto detection is not enabled![/bold yellow]")
            self.ui.print("Please enable it in Settings > Auto Detection Settings.")
            time.sleep(2)
            return
        
        # Start file watcher
        if not self.file_watcher.start():
            self.ui.print("[bold red]Failed to start file watcher![/bold red]")
            self.ui.print("Please check your settings and try again.")
            time.sleep(2)
            return
        
        # Show auto mode UI
        try:
            self.ui.show_auto_mode(self.process_new_screenshot)
        except KeyboardInterrupt:
            pass
        finally:
            # Stop file watcher
            self.file_watcher.stop()
    
    def run_manual_mode(self):
        """
        Run manual screenshot mode.
        """
        # Show manual mode UI and get file selection
        file_path = self.ui.show_manual_mode()
        
        if file_path:
            # Process the selected file
            output_path = self.process_screenshot(file_path)
            
            # Show processing information
            self.ui.show_processing(file_path, output_path)
    
    def run_settings(self):
        """
        Run settings menu.
        """
        while True:
            # Show settings menu
            choice = self.ui.show_settings_menu()
            
            if choice == "1":  # General Settings
                self.ui.show_general_settings()
            elif choice == "2":  # Border Settings
                self.ui.show_border_settings()
            elif choice == "3":  # Titlebar Settings
                self.ui.show_titlebar_settings()
            elif choice == "4":  # Footer Settings
                self.ui.show_footer_settings()
            elif choice == "5":  # Header Settings
                self.ui.show_header_settings()
            elif choice == "6":  # Custom Image Settings
                self.ui.show_custom_image_settings()
            elif choice == "7":  # Auto Detection Settings
                self.ui.show_auto_detection_settings()
            elif choice == "b":  # Back
                break
            
            # Reload configuration
            self.config = self.config_manager.config
            
            # Update image processor
            self.image_processor = ImageProcessor(self.config, self.theme_data)
            
            # Update file watcher
            self.file_watcher = FileWatcher(self.config["auto_detection"], self.process_new_screenshot)
    
    def run_themes(self):
        """
        Run themes menu.
        """
        while True:
            # Show themes menu
            choice = self.ui.show_theme_menu()
            
            if choice == "c":  # Create Custom Theme
                self.ui.create_custom_theme()
            elif choice == "b":  # Back
                break
            elif choice == "refresh":  # Theme changed, refresh
                # Reload theme data
                theme_id = self.config["appearance"]["theme"]
                self.theme_data = self.theme_manager.get_theme(theme_id)
                
                # Update image processor
                self.image_processor = ImageProcessor(self.config, self.theme_data)
    
    def process_new_screenshot(self, file_path: str):
        """
        Process a new screenshot.
        
        Args:
            file_path: Path to the screenshot file
        """
        self.ui.print(f"[bold]New screenshot detected: {os.path.basename(file_path)}[/bold]")
        
        # Process the screenshot
        output_path = self.process_screenshot(file_path)
        
        self.ui.print(f"[bold green]Processed: {os.path.basename(output_path)}[/bold green]")
        
        # Open the processed file if enabled
        if self.config["general"]["auto_open"]:
            self.open_file(output_path)
    
    def process_screenshot(self, file_path: str) -> str:
        """
        Process a screenshot.
        
        Args:
            file_path: Path to the screenshot file
            
        Returns:
            Path to the processed file
        """
        # Process the image
        output_path = self.image_processor.process_image(file_path)
        
        return output_path
    
    def open_file(self, file_path: str) -> bool:
        """
        Open a file with the default application with enhanced cross-platform support.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return False
            
        try:
            system = platform.system().lower()
            
            if system == "windows":
                # Windows
                os.startfile(file_path)
            elif system == "darwin":
                # macOS
                subprocess.run(["open", file_path], check=True)
            else:
                # Linux and other Unix-like systems
                if os.path.exists("/system/build.prop"):
                    # Android/Termux - try multiple methods
                    for cmd in ["termux-open", "am"]:
                        if shutil.which(cmd):
                            if cmd == "am":
                                subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", f"file://{file_path}"], check=True)
                            else:
                                subprocess.run([cmd, file_path], check=True)
                            return True
                    print("Warning: No suitable file opener found on Android")
                    return False
                else:
                    # Regular Linux - try multiple methods
                    for cmd in ["xdg-open", "gnome-open", "kde-open", "firefox", "chromium-browser"]:
                        if shutil.which(cmd):
                            subprocess.run([cmd, file_path], check=True)
                            return True
                    print("Warning: No suitable file opener found on Linux")
                    return False
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error opening file (command failed): {e}")
            return False
        except FileNotFoundError as e:
            print(f"Error opening file (command not found): {e}")
            return False
        except Exception as e:
            print(f"Error opening file: {e}")
            return False
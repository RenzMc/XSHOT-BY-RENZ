"""
Application UI for XShot

This module provides the main application UI for XShot.
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional, Callable, Tuple
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
from rich.live import Live
from rich.box import ROUNDED
from rich.columns import Columns
from rich.syntax import Syntax
from rich.markdown import Markdown

from xshot_py.ui.base_ui import BaseUI
from xshot_py.config.config_manager import ConfigManager
from xshot_py.themes.theme_manager import ThemeManager
from xshot_py.ui.footer_ui_helpers import FooterUIHelpers

class AppUI(BaseUI):
    """
    Main application UI for XShot.
    """
    
    def __init__(self, config_manager: ConfigManager, theme_manager: ThemeManager):
        """
        Initialize the application UI.
        
        Args:
            config_manager: Configuration manager instance
            theme_manager: Theme manager instance
        """
        super().__init__(config_manager, theme_manager)
        
        # Initialize footer/header UI helpers
        self.footer_helpers = FooterUIHelpers(self.console, self.config_manager)
    
    def show_main_menu(self) -> str:
        """
        Show the main menu and get user choice.
        
        Returns:
            User's menu choice
        """
        self.clear()
        self.print_header("XShot - Screenshot Enhancement Tool")
        
        # Create menu table
        table = Table(box=ROUNDED, expand=False, show_header=False, show_edge=False)
        table.add_column("Option", style="bold")
        table.add_column("Description")
        
        table.add_row("[1]", "Auto Screenshot Mode")
        table.add_row("[2]", "Manual Screenshot Mode")
        table.add_row("[3]", "Settings")
        table.add_row("[4]", "Themes")
        table.add_row("[5]", "Help")
        table.add_row("[q]", "Quit")
        
        # Show menu
        self.console.print(Panel(table, title="Main Menu", border_style="blue"))
        
        # Get user choice
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "q"], default="1")
        
        return choice
    
    def show_auto_mode(self, callback: Callable[[str], None]) -> None:
        """
        Show the auto screenshot mode UI.
        
        Args:
            callback: Function to call when a new screenshot is detected
        """
        self.clear()
        self.print_header("Auto Screenshot Mode")
        
        # Show instructions
        self.console.print(Panel(
            "XShot is now watching for new screenshots.\n"
            "Take a screenshot using your system's screenshot tool, and XShot will automatically enhance it.\n\n"
            "Press [bold]Ctrl+C[/bold] to return to the main menu.",
            title="Instructions",
            border_style="green"
        ))
        
        # Show watched directories
        watch_dirs = self.config_manager.safe_get_nested("auto_detection.watch_dirs", ["~/Pictures/Screenshots"])
        patterns = self.config_manager.safe_get_nested("auto_detection.file_patterns", ["*.png", "*.jpg", "*.jpeg"])
        
        watch_dirs_text = "\n".join([f"- {os.path.expanduser(d)}" for d in watch_dirs])
        patterns_text = ", ".join(patterns)
        
        self.console.print(Panel(
            f"Watching directories:\n{watch_dirs_text}\n\nFile patterns: {patterns_text}",
            title="Watch Settings",
            border_style="blue"
        ))
        
        # Wait for Ctrl+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    
    def show_manual_mode(self) -> Optional[str]:
        """
        Show the manual screenshot mode UI.
        
        Returns:
            Selected file path or None if cancelled
        """
        self.clear()
        self.print_header("Manual Screenshot Mode")
        
        # Show instructions
        self.console.print(Panel(
            "Select a screenshot file to enhance.\n"
            "Enter the full path to the file, or leave empty to cancel.",
            title="Instructions",
            border_style="green"
        ))
        
        # Get file path
        file_path = Prompt.ask("Enter file path", default="")
        
        if not file_path:
            return None
        
        # Expand user directory
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            self.console.print(f"[bold red]Error:[/bold red] File not found: {file_path}")
            time.sleep(2)
            return None
        
        return file_path
    
    def show_processing(self, input_path: str, output_path: str) -> None:
        """
        Show processing information.
        
        Args:
            input_path: Path to the input file
            output_path: Path to the output file
        """
        self.clear()
        self.print_header("Processing Complete")
        
        # Show processing information
        self.console.print(Panel(
            f"Input file: [bold]{os.path.basename(input_path)}[/bold]\n"
            f"Output file: [bold]{os.path.basename(output_path)}[/bold]\n\n"
            f"Output saved to: [bold]{output_path}[/bold]",
            title="Processing Information",
            border_style="green"
        ))
        
        # Show options
        self.console.print("\nPress Enter to continue...")
        input()
    
    def show_settings_menu(self) -> str:
        """
        Show the settings menu and get user choice.
        
        Returns:
            User's menu choice
        """
        self.clear()
        self.print_header("Settings")
        
        # Create menu table
        table = Table(box=ROUNDED, expand=False, show_header=False, show_edge=False)
        table.add_column("Option", style="bold")
        table.add_column("Description")
        
        table.add_row("[1]", "General Settings")
        table.add_row("[2]", "Border Settings")
        table.add_row("[3]", "Titlebar Settings")
        table.add_row("[4]", "Footer Settings")
        table.add_row("[5]", "Header Settings")
        table.add_row("[6]", "Custom Image Settings")
        table.add_row("[7]", "Auto Detection Settings")
        table.add_row("[b]", "Back to Main Menu")
        
        # Show menu
        self.console.print(Panel(table, title="Settings Menu", border_style="blue"))
        
        # Get user choice
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "b"], default="b")
        
        return choice
    
    def show_general_settings(self) -> None:
        """
        Show and edit general settings.
        """
        self.clear()
        self.print_header("General Settings")
        
        # Get current settings
        config = self.config_manager.get_section("general")
        
        # Show current settings
        self.console.print(Panel(
            f"Screenshot Directory: [bold]{config['screenshot_dir']}[/bold]\n"
            f"Output Directory: [bold]{config['output_dir']}[/bold]\n"
            f"Backup Directory: [bold]{config['backup_dir']}[/bold]\n"
            f"Auto Open: [bold]{'Yes' if config['auto_open'] else 'No'}[/bold]\n"
            f"Auto Backup: [bold]{'Yes' if config['auto_backup'] else 'No'}[/bold]",
            title="Current Settings",
            border_style="blue"
        ))
        
        # Edit settings
        self.console.print("\n[bold]Edit Settings:[/bold]")
        
        # Screenshot directory
        screenshot_dir = Prompt.ask("Screenshot Directory", default=config["screenshot_dir"])
        config["screenshot_dir"] = screenshot_dir
        
        # Output directory
        output_dir = Prompt.ask("Output Directory", default=config["output_dir"])
        config["output_dir"] = output_dir
        
        # Backup directory
        backup_dir = Prompt.ask("Backup Directory", default=config["backup_dir"])
        config["backup_dir"] = backup_dir
        
        # Auto open
        auto_open = Confirm.ask("Auto Open", default=config["auto_open"])
        config["auto_open"] = auto_open
        
        # Auto backup
        auto_backup = Confirm.ask("Auto Backup", default=config["auto_backup"])
        config["auto_backup"] = auto_backup
        
        # Save settings
        self.config_manager.save_config()
        
        self.console.print("\n[bold green]Settings saved![/bold green]")
        time.sleep(1)
    
    def show_border_settings(self) -> None:
        """
        Show and edit border settings.
        """
        self.clear()
        self.print_header("Border Settings")
        
        # Get current settings
        config = self.config_manager.get_section("border")
        
        # Show current settings
        self.console.print(Panel(
            f"Border Size: [bold]{config['size']}px[/bold]\n"
            f"Border Radius: [bold]{config['radius']}px[/bold]\n"
            f"Dark Theme Border Color: [bold]{config['color_dark']}[/bold]\n"
            f"Light Theme Border Color: [bold]{config['color_light']}[/bold]\n"
            f"Shadow Size: [bold]{config['shadow_size']}[/bold]\n"
            f"Shadow Color: [bold]{config['shadow_color']}[/bold]",
            title="Current Settings",
            border_style="blue"
        ))
        
        # Edit settings
        self.console.print("\n[bold]Edit Settings:[/bold]")
        
        # Border size
        border_size = int(Prompt.ask("Border Size (px)", default=str(config["size"])))
        config["size"] = border_size
        
        # Border radius
        border_radius = int(Prompt.ask("Border Radius (px)", default=str(config["radius"])))
        config["radius"] = border_radius
        
        # Dark theme border color
        color_dark = Prompt.ask("Dark Theme Border Color", default=config["color_dark"])
        config["color_dark"] = color_dark
        
        # Light theme border color
        color_light = Prompt.ask("Light Theme Border Color", default=config["color_light"])
        config["color_light"] = color_light
        
        # Shadow size
        shadow_size = Prompt.ask("Shadow Size", default=config["shadow_size"])
        config["shadow_size"] = shadow_size
        
        # Shadow color
        shadow_color = Prompt.ask("Shadow Color", default=config["shadow_color"])
        config["shadow_color"] = shadow_color
        
        # Save settings
        self.config_manager.save_config()
        
        self.console.print("\n[bold green]Settings saved![/bold green]")
        time.sleep(1)
    
    def show_titlebar_settings(self) -> None:
        """
        Show and edit titlebar settings.
        """
        self.clear()
        self.print_header("Titlebar Settings")
        
        # Get current settings
        config = self.config_manager.get_section("titlebar")
        
        # Show current settings
        self.console.print(Panel(
            f"Enabled: [bold]{'Yes' if config['enabled'] else 'No'}[/bold]\n"
            f"Font Size: [bold]{config['size']}px[/bold]\n"
            f"Show Device Info: [bold]{'Yes' if config['show_device_info'] else 'No'}[/bold]\n"
            f"Custom Text: [bold]{config['custom_text'] if config['custom_text'] else 'None'}[/bold]",
            title="Current Settings",
            border_style="blue"
        ))
        
        # Edit settings
        self.console.print("\n[bold]Edit Settings:[/bold]")
        
        # Enabled
        enabled = Confirm.ask("Enabled", default=config["enabled"])
        config["enabled"] = enabled
        
        # Font size
        font_size = int(Prompt.ask("Font Size (px)", default=str(config["size"])))
        config["size"] = font_size
        
        # Show device info
        show_device_info = Confirm.ask("Show Device Info", default=config["show_device_info"])
        config["show_device_info"] = show_device_info
        
        # Custom text
        custom_text = Prompt.ask("Custom Text (leave empty for none)", default=config["custom_text"] if config["custom_text"] else "")
        config["custom_text"] = custom_text if custom_text else None
        
        # Save settings
        self.config_manager.save_config()
        
        self.console.print("\n[bold green]Settings saved![/bold green]")
        time.sleep(1)
    
    def show_footer_settings(self) -> None:
        """
        Show and edit advanced footer settings with comprehensive customization.
        """
        while True:
            self.clear()
            self.print_header("Advanced Footer Settings")
            
            # Get current settings
            config = self.config_manager.get_section("footer")
            
            # Show current settings overview
            self.console.print(Panel(
                f"[bold]Basic Settings:[/bold]\n"
                f"Enabled: [bold]{'Yes' if config['enabled'] else 'No'}[/bold]\n"
                f"Text: [bold]{config['text']}[/bold]\n"
                f"Position: [bold]{config['position']}[/bold]\n"
                f"Font: [bold]{config.get('font_family', 'mono')} {config.get('font_style', 'normal')}[/bold]\n"
                f"Size: [bold]{config['size']}px[/bold]\n"
                f"Color: [bold]{config['color']}[/bold]\n\n"
                f"[bold]Advanced Features:[/bold]\n"
                f"Text Shadow: [bold]{'Yes' if config.get('text_shadow', False) else 'No'}[/bold]\n"
                f"Text Outline: [bold]{'Yes' if config.get('text_outline', False) else 'No'}[/bold]\n"
                f"Background: [bold]{'Yes' if config.get('background_enabled', False) else 'No'}[/bold]\n"
                f"Show Time: [bold]{'Yes' if config['show_time'] else 'No'}[/bold]\n"
                f"Custom Elements: [bold]{len(config.get('custom_elements', []))}[/bold]",
                title="Current Footer Settings",
                border_style="blue"
            ))
            
            # Menu options
            self.console.print("\n[bold]Customization Options:[/bold]")
            self.console.print("[1] Basic Settings (text, position, size, color)")
            self.console.print("[2] Font & Style Options") 
            self.console.print("[3] Advanced Effects (shadow, outline)")
            self.console.print("[4] Background & Border")
            self.console.print("[5] Time Display Settings")
            self.console.print("[6] Custom Text Elements")
            self.console.print("[7] Quick Style Presets")
            self.console.print("[8] Preview Current Settings")
            self.console.print("[b] Back to Settings")
            
            choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "b"], default="b")
            
            if choice == "1":
                self.footer_helpers._edit_footer_basic_settings(config)
            elif choice == "2":
                self.footer_helpers._edit_footer_font_settings(config)
            elif choice == "3":
                self.footer_helpers._edit_footer_effects(config)
            elif choice == "4":
                self.footer_helpers._edit_footer_background(config)
            elif choice == "5":
                self.footer_helpers._edit_footer_time_settings(config)
            elif choice == "6":
                self.footer_helpers._edit_footer_custom_elements(config)
            elif choice == "7":
                self.footer_helpers._apply_footer_presets(config)
            elif choice == "8":
                self.footer_helpers._preview_footer_settings(config)
            elif choice == "b":
                break
                
            # Auto-save after each change
            self.config_manager.save_config()
    
    def show_header_settings(self) -> None:
        """
        Show and edit advanced header settings with comprehensive customization.
        """
        while True:
            self.clear()
            self.print_header("Advanced Header Settings")
            
            # Get current settings safely
            config = self.config_manager.get_section("header", {
                "enabled": False,
                "text": "XShot Screenshot",
                "position": "top",
                "size": 22,
                "color": "#000000",
                "show_time": False,
                "time_format": "%a %d.%b.%Y %H:%M",
                "time_size": 18,
                "font_family": "sans",
                "font_style": "bold",
                "text_shadow": False,
                "shadow_color": "#FFFFFF",
                "shadow_offset": [2, 2],
                "text_outline": False,
                "outline_color": "#FFFFFF",
                "outline_width": 1,
                "background_enabled": False,
                "background_color": "#000000",
                "background_opacity": 128,
                "background_padding": [10, 5],
                "background_border": False,
                "border_color": "#FFFFFF",
                "border_width": 1,
                "custom_elements": []
            })
            
            # Ensure header config exists in the main config
            if self.config_manager.config and "header" not in self.config_manager.config:
                self.config_manager.config["header"] = config
            
            # Show current settings overview
            self.console.print(Panel(
                f"[bold]Basic Settings:[/bold]\n"
                f"Enabled: [bold]{'Yes' if config['enabled'] else 'No'}[/bold]\n"
                f"Text: [bold]{config['text']}[/bold]\n"
                f"Position: [bold]{config['position']}[/bold]\n"
                f"Font: [bold]{config.get('font_family', 'sans')} {config.get('font_style', 'bold')}[/bold]\n"
                f"Size: [bold]{config['size']}px[/bold]\n"
                f"Color: [bold]{config['color']}[/bold]\n\n"
                f"[bold]Advanced Features:[/bold]\n"
                f"Text Shadow: [bold]{'Yes' if config.get('text_shadow', False) else 'No'}[/bold]\n"
                f"Text Outline: [bold]{'Yes' if config.get('text_outline', False) else 'No'}[/bold]\n"
                f"Background: [bold]{'Yes' if config.get('background_enabled', False) else 'No'}[/bold]\n"
                f"Show Time: [bold]{'Yes' if config['show_time'] else 'No'}[/bold]\n"
                f"Custom Elements: [bold]{len(config.get('custom_elements', []))}[/bold]",
                title="Current Header Settings",
                border_style="cyan"
            ))
            
            # Menu options
            self.console.print("\n[bold]Customization Options:[/bold]")
            self.console.print("[1] Basic Settings (text, position, size, color)")
            self.console.print("[2] Font & Style Options") 
            self.console.print("[3] Advanced Effects (shadow, outline)")
            self.console.print("[4] Background & Border")
            self.console.print("[5] Time Display Settings")
            self.console.print("[6] Custom Text Elements")
            self.console.print("[7] Quick Style Presets")
            self.console.print("[8] Preview Current Settings")
            self.console.print("[b] Back to Settings")
            
            choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "b"], default="b")
            
            if choice == "1":
                self.footer_helpers._edit_footer_basic_settings(config)
            elif choice == "2":
                self.footer_helpers._edit_footer_font_settings(config)
            elif choice == "3":
                self.footer_helpers._edit_footer_effects(config)
            elif choice == "4":
                self.footer_helpers._edit_footer_background(config)
            elif choice == "5":
                self.footer_helpers._edit_footer_time_settings(config)
            elif choice == "6":
                self.footer_helpers._edit_footer_custom_elements(config)
            elif choice == "7":
                self.footer_helpers._apply_footer_presets(config)
            elif choice == "8":
                self.footer_helpers._preview_footer_settings(config)
            elif choice == "b":
                break
                
            # Auto-save after each change
            self.config_manager.save_config()
    
    def show_text_watermark_settings(self) -> None:
        """
        Show comprehensive text watermark settings (headers and footers).
        """
        while True:
            self.clear()
            self.print_header("Text Watermark Settings")
            
            # Show overview of both header and footer
            footer_config = self.config_manager.get_section("footer")
            header_config = self.config_manager.get_section("header", {"enabled": False})
            
            self.console.print(Panel(
                f"[bold]Footer:[/bold]\n"
                f"  Enabled: {'Yes' if footer_config['enabled'] else 'No'}\n"
                f"  Text: {footer_config['text']}\n"
                f"  Position: {footer_config['position']}\n"
                f"  Effects: {('Shadow' if footer_config.get('text_shadow', False) else '') + (' Outline' if footer_config.get('text_outline', False) else '') or 'None'}\n\n"
                f"[bold]Header:[/bold]\n"
                f"  Enabled: {'Yes' if header_config.get('enabled', False) else 'No'}\n"
                f"  Text: {header_config.get('text', 'XShot Screenshot')}\n"
                f"  Position: {header_config.get('position', 'top')}\n"
                f"  Effects: {('Shadow' if header_config.get('text_shadow', False) else '') + (' Outline' if header_config.get('text_outline', False) else '') or 'None'}",
                title="Text Watermark Overview",
                border_style="magenta"
            ))
            
            # Menu options
            self.console.print("\n[bold]Options:[/bold]")
            self.console.print("[1] Footer Settings")
            self.console.print("[2] Header Settings")
            self.console.print("[3] Quick Setup Wizard")
            self.console.print("[b] Back to Settings")
            
            choice = Prompt.ask("Choose option", choices=["1", "2", "3", "b"], default="b")
            
            if choice == "1":
                self.show_footer_settings()
            elif choice == "2":
                self.show_header_settings()
            elif choice == "3":
                self._text_watermark_wizard()
            elif choice == "b":
                break
    
    def _text_watermark_wizard(self) -> None:
        """
        Quick setup wizard for text watermarks.
        """
        self.clear()
        self.print_header("Text Watermark Setup Wizard")
        
        self.console.print("[bold cyan]This wizard will help you quickly setup headers and footers.[/bold cyan]\n")
        
        # Footer setup
        if Confirm.ask("Configure footer watermark?", default=True):
            footer_config = self.config_manager.get_section("footer")
            footer_config["enabled"] = True
            footer_config["text"] = Prompt.ask("Footer text", default="Shot by XShot")
            
            positions = ["bottom", "bottom-left", "bottom-right"]
            footer_config["position"] = Prompt.ask("Footer position", choices=positions, default="bottom")
            
        # Header setup
        if Confirm.ask("Configure header watermark?", default=False):
            if "header" not in self.config_manager.config:
                self.config_manager.config["header"] = {
                    "enabled": False,
                    "text": "XShot Screenshot",
                    "position": "top",
                    "size": 22,
                    "color": "#000000",
                    "show_time": False,
                    "time_format": "%a %d.%b.%Y %H:%M",
                    "time_size": 18,
                    "font_family": "sans",
                    "font_style": "bold"
                }
            
            header_config = self.config_manager.config["header"]
            header_config["enabled"] = True
            header_config["text"] = Prompt.ask("Header text", default="XShot Screenshot")
            
            positions = ["top", "top-left", "top-right"]
            header_config["position"] = Prompt.ask("Header position", choices=positions, default="top")
        
        # Save and confirm
        self.config_manager.save_config()
        self.console.print("\n[bold green]Text watermark setup complete![/bold green]")
        time.sleep(2)
    
    def show_custom_image_settings(self) -> None:
        """
        Show and edit custom image settings.
        """
        self.clear()
        self.print_header("Custom Image Settings")
        
        # Get current settings
        config = self.config_manager.get_section("custom_image")
        
        # Show current settings
        self.console.print(Panel(
            f"Enabled: [bold]{'Yes' if config['enabled'] else 'No'}[/bold]\n"
            f"Image Path: [bold]{config['path'] if config['path'] else 'None'}[/bold]\n"
            f"Position: [bold]{config['position']}[/bold]\n"
            f"Size: [bold]{config['size']}px[/bold]\n"
            f"Padding: [bold]{config['padding']}px[/bold]",
            title="Current Settings",
            border_style="blue"
        ))
        
        # Edit settings
        self.console.print("\n[bold]Edit Settings:[/bold]")
        
        # Enabled
        enabled = Confirm.ask("Enabled", default=config["enabled"])
        config["enabled"] = enabled
        
        # Image path
        image_path = Prompt.ask("Image Path (leave empty for none)", default=config["path"] if config["path"] else "")
        config["path"] = image_path if image_path else None
        
        # Position
        position = Prompt.ask("Position", choices=["top-left", "top-right", "bottom-left", "bottom-right"], default=config["position"])
        config["position"] = position
        
        # Size
        size = int(Prompt.ask("Size (px)", default=str(config["size"])))
        config["size"] = size
        
        # Padding
        padding = int(Prompt.ask("Padding (px)", default=str(config["padding"])))
        config["padding"] = padding
        
        # Save settings
        self.config_manager.save_config()
        
        self.console.print("\n[bold green]Settings saved![/bold green]")
        time.sleep(1)
    
    def show_auto_detection_settings(self) -> None:
        """
        Show and edit auto detection settings.
        """
        self.clear()
        self.print_header("Auto Detection Settings")
        
        # Get current settings
        config = self.config_manager.get_section("auto_detection")
        
        # Show current settings
        watch_dirs = "\n".join([f"- {d}" for d in config["watch_dirs"]])
        file_patterns = ", ".join(config["file_patterns"])
        
        self.console.print(Panel(
            f"Enabled: [bold]{'Yes' if config['enabled'] else 'No'}[/bold]\n\n"
            f"Watch Directories:\n[bold]{watch_dirs}[/bold]\n\n"
            f"File Patterns: [bold]{file_patterns}[/bold]",
            title="Current Settings",
            border_style="blue"
        ))
        
        # Edit settings
        self.console.print("\n[bold]Edit Settings:[/bold]")
        
        # Enabled
        enabled = Confirm.ask("Enabled", default=config["enabled"])
        config["enabled"] = enabled
        
        # Watch directories
        self.console.print("\nCurrent watch directories:")
        for i, dir_path in enumerate(config["watch_dirs"]):
            self.console.print(f"[{i+1}] {dir_path}")
        
        self.console.print("\nOptions:")
        self.console.print("[a] Add directory")
        self.console.print("[r] Remove directory")
        self.console.print("[c] Continue")
        
        while True:
            choice = Prompt.ask("Choose an option", choices=["a", "r", "c"], default="c")
            
            if choice == "a":
                dir_path = Prompt.ask("Enter directory path")
                config["watch_dirs"].append(dir_path)
            elif choice == "r":
                if not config["watch_dirs"]:
                    self.console.print("[bold yellow]No directories to remove![/bold yellow]")
                    continue
                
                index = int(Prompt.ask("Enter directory number to remove", choices=[str(i+1) for i in range(len(config["watch_dirs"]))]))
                config["watch_dirs"].pop(index - 1)
            else:
                break
            
            # Show updated list
            self.console.print("\nUpdated watch directories:")
            for i, dir_path in enumerate(config["watch_dirs"]):
                self.console.print(f"[{i+1}] {dir_path}")
            
            self.console.print("\nOptions:")
            self.console.print("[a] Add directory")
            self.console.print("[r] Remove directory")
            self.console.print("[c] Continue")
        
        # File patterns
        self.console.print("\nCurrent file patterns:")
        for i, pattern in enumerate(config["file_patterns"]):
            self.console.print(f"[{i+1}] {pattern}")
        
        self.console.print("\nOptions:")
        self.console.print("[a] Add pattern")
        self.console.print("[r] Remove pattern")
        self.console.print("[c] Continue")
        
        while True:
            choice = Prompt.ask("Choose an option", choices=["a", "r", "c"], default="c")
            
            if choice == "a":
                pattern = Prompt.ask("Enter file pattern (e.g., *.png)")
                config["file_patterns"].append(pattern)
            elif choice == "r":
                if not config["file_patterns"]:
                    self.console.print("[bold yellow]No patterns to remove![/bold yellow]")
                    continue
                
                index = int(Prompt.ask("Enter pattern number to remove", choices=[str(i+1) for i in range(len(config["file_patterns"]))]))
                config["file_patterns"].pop(index - 1)
            else:
                break
            
            # Show updated list
            self.console.print("\nUpdated file patterns:")
            for i, pattern in enumerate(config["file_patterns"]):
                self.console.print(f"[{i+1}] {pattern}")
            
            self.console.print("\nOptions:")
            self.console.print("[a] Add pattern")
            self.console.print("[r] Remove pattern")
            self.console.print("[c] Continue")
        
        # Save settings
        self.config_manager.save_config()
        
        self.console.print("\n[bold green]Settings saved![/bold green]")
        time.sleep(1)
    
    def show_theme_menu(self) -> str:
        """
        Show the theme menu and get user choice.
        
        Returns:
            User's menu choice
        """
        self.clear()
        self.print_header("Theme Settings")
        
        # Get current theme
        current_theme_id = self.config_manager.config["appearance"]["theme"]
        
        # Get theme list
        theme_list = self.theme_manager.get_theme_list()
        
        # Show current theme
        current_theme = next((t for t in theme_list if t["id"] == current_theme_id), None)
        if current_theme:
            self.console.print(Panel(
                f"Current Theme: [bold]{current_theme['name']}[/bold]\n"
                f"Description: {current_theme['description']}\n"
                f"Type: {current_theme['type']}",
                title="Current Theme",
                border_style="blue"
            ))
        
        # Create theme table
        table = Table(box=ROUNDED, expand=False)
        table.add_column("ID", style="bold")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Type")
        table.add_column("Current")
        
        for theme in theme_list:
            is_current = theme["id"] == current_theme_id
            table.add_row(
                theme["id"],
                theme["name"],
                theme["description"],
                theme["type"],
                "✓" if is_current else ""
            )
        
        # Show theme list
        self.console.print(Panel(table, title="Available Themes", border_style="blue"))
        
        # Show options
        self.console.print("\n[bold]Options:[/bold]")
        self.console.print("[theme_id] Select theme (e.g., 'dark', 'light', 'nord', 'dracula')")
        self.console.print("[c] Advanced Theme Creator")
        self.console.print("[s] Simple Theme Creator")
        self.console.print("[b] Back to Settings")
        
        # Get user choice
        choice = Prompt.ask("Choose an option", default="b")
        
        # Handle theme selection
        if choice in [t["id"] for t in theme_list]:
            self.config_manager.config["appearance"]["theme"] = choice
            self.config_manager.save_config()
            self.console.print(f"\n[bold green]Theme changed to {choice}![/bold green]")
            time.sleep(1)
            return "refresh"
        elif choice == "c":  # Advanced Theme Creator
            result = self.show_custom_theme_creator()
            if result == "refresh":
                return "refresh"
        elif choice == "s":  # Simple Theme Creator
            result = self.create_custom_theme()
            if result == "refresh":
                return "refresh"
        
        return choice
    
    def create_custom_theme(self) -> None:
        """
        Create a custom theme.
        """
        self.clear()
        self.print_header("Create Custom Theme")
        
        # Get theme information
        self.console.print("[bold]Theme Information:[/bold]")
        theme_id = Prompt.ask("Theme ID (lowercase, no spaces)")
        theme_name = Prompt.ask("Theme Name")
        theme_description = Prompt.ask("Theme Description")
        
        # Create theme data structure
        theme_data = {
            "name": theme_name,
            "description": theme_description,
            "colors": {
                "background": "#1E222B",
                "foreground": "#F8F9FA",
                "accent": "#59d6ff",
                "border": "#3d465c",
                "shadow": "#000000",
                "success": "#38d13e",
                "error": "#ff5f56",
                "warning": "#FFBD2E",
                "info": "#59d6ff",
                "muted": "#e6e6e6",
            },
            "ui": {
                "header_bg": "#1E222B",
                "header_fg": "#F8F9FA",
                "footer_bg": "#1E222B",
                "footer_fg": "#F8F9FA",
                "button_bg": "#3d465c",
                "button_fg": "#F8F9FA",
                "button_accent": "#59d6ff",
                "input_bg": "#2A2E39",
                "input_fg": "#F8F9FA",
                "panel_bg": "#2A2E39",
                "panel_fg": "#F8F9FA",
            }
        }
        
        # Edit colors
        self.console.print("\n[bold]Edit Colors:[/bold]")
        for key, value in theme_data["colors"].items():
            theme_data["colors"][key] = Prompt.ask(f"Color: {key}", default=value)
        
        # Edit UI colors
        self.console.print("\n[bold]Edit UI Colors:[/bold]")
        for key, value in theme_data["ui"].items():
            theme_data["ui"][key] = Prompt.ask(f"UI Color: {key}", default=value)
        
        # Save theme
        if self.theme_manager.save_custom_theme(theme_id, theme_data):
            self.console.print("\n[bold green]Theme created successfully![/bold green]")
            
            # Ask if user wants to apply the theme
            if Confirm.ask("Apply this theme now?"):
                self.config_manager.config["appearance"]["theme"] = theme_id
                self.config_manager.save_config()
                self.console.print("[bold green]Theme applied![/bold green]")
        else:
            self.console.print("\n[bold red]Error creating theme![/bold red]")
        
        time.sleep(1)
    
    def show_help(self) -> None:
        """
        Show help information.
        """
        self.clear()
        self.print_header("Help")
        
        help_text = """
        # XShot Help
        
        XShot is a screenshot enhancement tool that adds professional-looking borders, 
        titlebar, and other elements to your screenshots.
        
        ## Modes
        
        ### Auto Screenshot Mode
        
        In this mode, XShot watches specified directories for new screenshots and 
        automatically enhances them when detected.
        
        ### Manual Screenshot Mode
        
        In this mode, you can select a specific image file to enhance.
        
        ## Settings
        
        XShot offers various settings to customize the appearance of your enhanced screenshots:
        
        - **General Settings**: Configure basic application settings
        - **Border Settings**: Customize the border appearance
        - **Titlebar Settings**: Configure the titlebar
        - **Footer Settings**: Customize the footer text and appearance
        - **Custom Image Settings**: Add a custom image (like a logo) to your screenshots
        - **Auto Detection Settings**: Configure which directories to watch for new screenshots
        
        ## Themes
        
        XShot comes with several built-in themes:
        
        - **Dark**: Default dark theme
        - **Light**: Clean light theme
        - **Nord**: Arctic-inspired theme
        - **Dracula**: Dark theme with vibrant colors
        
        You can also create your own custom themes.
        """
        
        self.console.print(Markdown(help_text))
        
        self.console.print("\nPress Enter to continue...")
        input()
    def show_custom_theme_creator(self) -> str:
        """
        Show the advanced custom theme creator interface.
        
        Returns:
            User's choice or action result
        """
        from xshot_py.themes.theme_manager import CustomThemeCreator
        
        # Initialize the theme creator
        theme_creator = CustomThemeCreator(self.theme_manager)
        
        while True:
            self.clear()
            self.print_header("Advanced Theme Creator")
            
            # Show current theme preview
            preview = theme_creator.get_theme_preview()
            current_theme = preview["theme_data"]
            
            # Create preview panel
            preview_table = Table(box=ROUNDED, expand=False, show_header=False)
            preview_table.add_column("Element", style="bold")
            preview_table.add_column("Color")
            
            preview_table.add_row("Background", current_theme["colors"]["background"])
            preview_table.add_row("Foreground", current_theme["colors"]["foreground"])
            preview_table.add_row("Accent", current_theme["colors"]["accent"])
            preview_table.add_row("Border", current_theme["colors"]["border"])
            
            self.console.print(Panel(preview_table, title=f"Theme Preview: {current_theme['name']}", border_style="blue"))
            
            # Show main menu
            menu_table = Table(box=ROUNDED, expand=False, show_header=False, show_edge=False)
            menu_table.add_column("Option", style="bold")
            menu_table.add_column("Description")
            
            menu_table.add_row("[1]", "Color Palette Presets")
            menu_table.add_row("[2]", "Custom Color Editor")
            menu_table.add_row("[3]", "Color Harmony Generator")
            menu_table.add_row("[4]", "Gradient Theme Creator")
            menu_table.add_row("[5]", "Border & Shape Options")
            menu_table.add_row("[6]", "Font Family Selection")
            menu_table.add_row("[7]", "Save Custom Theme")
            menu_table.add_row("[8]", "Load Theme for Editing")
            menu_table.add_row("[9]", "Reset to Default")
            menu_table.add_row("[p]", "Live Preview")
            menu_table.add_row("[b]", "Back to Theme Menu")
            
            self.console.print(Panel(menu_table, title="Theme Creator Options", border_style="green"))
            
            choice = Prompt.ask("Choose an option", 
                              choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "p", "b"], 
                              default="b")
            
            if choice == "1":
                self._show_color_palette_presets(theme_creator)
            elif choice == "2":
                self._show_custom_color_editor(theme_creator)
            elif choice == "3":
                self._show_color_harmony_generator(theme_creator)
            elif choice == "4":
                self._show_gradient_theme_creator(theme_creator)
            elif choice == "5":
                self._show_border_shape_options(theme_creator)
            elif choice == "6":
                self._show_font_family_selection(theme_creator)
            elif choice == "7":
                success = self._save_custom_theme(theme_creator)
                if success:
                    self.console.print("[bold green]Theme saved successfully![/bold green]")
                    time.sleep(2)
            elif choice == "8":
                self._load_theme_for_editing(theme_creator)
            elif choice == "9":
                theme_creator.reset_theme()
                self.console.print("[bold yellow]Theme reset to default![/bold yellow]")
                time.sleep(1)
            elif choice == "p":
                self._show_live_preview(theme_creator)
            elif choice == "b":
                break
        
        return "refresh"
    
    def show_auto_detection_settings(self) -> None:
        """
        Show and edit auto detection settings.
        """
        self.clear()
        self.print_header("Auto Detection Settings")
        
        # Get current settings
        config = self.config_manager.get_section("auto_detection")
        
        # Show current settings
        self.console.print(Panel(
            f"Enabled: [bold]{'Yes' if config['enabled'] else 'No'}[/bold]\n"
            f"Watch Directories: [bold]{', '.join(config['watch_dirs'])}[/bold]\n"
            f"File Patterns: [bold]{', '.join(config['file_patterns'])}[/bold]",
            title="Current Settings",
            border_style="blue"
        ))
        
        # Edit settings
        self.console.print("\n[bold]Edit Settings:[/bold]")
        
        # Enabled
        enabled = Confirm.ask("Enable auto detection", default=config["enabled"])
        config["enabled"] = enabled
        
        if enabled:
            # Watch directories
            dirs_str = Prompt.ask("Watch directories (comma-separated)", default=",".join(config["watch_dirs"]))
            config["watch_dirs"] = [d.strip() for d in dirs_str.split(",") if d.strip()]
            
            # File patterns
            patterns_str = Prompt.ask("File patterns (comma-separated)", default=",".join(config["file_patterns"]))
            config["file_patterns"] = [p.strip() for p in patterns_str.split(",") if p.strip()]
        
        # Save settings
        self.config_manager.save_config()
        
        self.console.print("\n[bold green]Settings saved![/bold green]")
        time.sleep(1)

    def _show_color_palette_presets(self, theme_creator) -> None:
        """Show color palette presets selection."""
        self.clear()
        self.print_header("Color Palette Presets")
        
        # Show available palettes
        palettes = list(theme_creator.color_palettes.keys())
        
        palette_table = Table(box=ROUNDED, expand=False)
        palette_table.add_column("Option", style="bold")
        palette_table.add_column("Palette Name")
        palette_table.add_column("Description")
        
        descriptions = {
            "Material Design": "Google's Material Design colors",
            "Nord": "Arctic, north-bluish color palette",
            "Dracula": "Dark theme with vibrant colors",
            "Cyberpunk": "Futuristic neon colors",
            "Sunset": "Warm, sunset-inspired colors"
        }
        
        for i, palette_name in enumerate(palettes, 1):
            palette_table.add_row(
                f"[{i}]",
                palette_name,
                descriptions.get(palette_name, "Custom color palette")
            )
        
        self.console.print(Panel(palette_table, title="Available Color Palettes", border_style="cyan"))
        
        choices = [str(i) for i in range(1, len(palettes) + 1)] + ["b"]
        choice = Prompt.ask("Choose a palette", choices=choices, default="b")
        
        if choice != "b":
            palette_name = palettes[int(choice) - 1]
            success = theme_creator.apply_color_palette(palette_name)
            if success:
                self.console.print(f"[bold green]Applied {palette_name} palette![/bold green]")
                time.sleep(2)

    def _show_custom_color_editor(self, theme_creator) -> None:
        """Show custom color editor interface."""
        self.clear()
        self.print_header("Custom Color Editor")
        
        # Show current colors
        current_theme = theme_creator.current_theme
        
        color_table = Table(box=ROUNDED, expand=False)
        color_table.add_column("Section", style="bold")
        color_table.add_column("Element", style="bold")
        color_table.add_column("Current Color")
        
        # Add color elements
        for section in ["colors", "ui"]:
            for element, color in current_theme[section].items():
                color_table.add_row(
                    section.title(),
                    element.replace("_", " ").title(),
                    color
                )
        
        self.console.print(Panel(color_table, title="Current Colors", border_style="blue"))
        
        # Get user selection
        section = Prompt.ask("Select section", choices=["colors", "ui", "back"], default="back")
        if section == "back":
            return
        
        elements = list(current_theme[section].keys())
        element_choices = [str(i) for i in range(1, len(elements) + 1)] + ["back"]
        
        self.console.print("\nAvailable elements:")
        for i, element in enumerate(elements, 1):
            self.console.print(f"[{i}] {element.replace('_', ' ').title()}")
        
        choice = Prompt.ask("Select element to modify", choices=element_choices, default="back")
        if choice == "back":
            return
        
        element = elements[int(choice) - 1]
        current_color = current_theme[section][element]
        
        self.console.print(f"\nCurrent color for {element}: {current_color}")
        
        new_color = Prompt.ask("Enter new color (hex format, e.g., #FF6B35)", default=current_color)
        
        success = theme_creator.customize_color(element, new_color, section)
        if success:
            self.console.print(f"[bold green]Color updated successfully![/bold green]")
        else:
            self.console.print(f"[bold red]Invalid color format![/bold red]")
        
        time.sleep(2)

    def _show_color_harmony_generator(self, theme_creator) -> None:
        """Show color harmony generator interface."""
        self.clear()
        self.print_header("Color Harmony Generator")
        
        self.console.print(Panel(
            "Generate harmonious color schemes based on color theory.\n"
            "Enter a base color and choose a harmony type to generate matching colors.",
            title="Color Harmony",
            border_style="magenta"
        ))
        
        base_color = Prompt.ask("Enter base color (hex format, e.g., #FF6B35)", default="#FF6B35")
        
        harmony_types = ["complementary", "triadic", "analogous", "monochromatic"]
        harmony_table = Table(box=ROUNDED, expand=False, show_header=False)
        harmony_table.add_column("Option", style="bold")
        harmony_table.add_column("Type")
        harmony_table.add_column("Description")
        
        harmony_table.add_row("[1]", "Complementary", "Opposite colors on color wheel")
        harmony_table.add_row("[2]", "Triadic", "Three evenly spaced colors")
        harmony_table.add_row("[3]", "Analogous", "Adjacent colors on color wheel")
        harmony_table.add_row("[4]", "Monochromatic", "Variations of same hue")
        
        self.console.print(Panel(harmony_table, title="Harmony Types", border_style="cyan"))
        
        choice = Prompt.ask("Choose harmony type", choices=["1", "2", "3", "4", "b"], default="1")
        if choice == "b":
            return
        
        harmony_type = harmony_types[int(choice) - 1]
        harmony_colors = theme_creator.generate_color_harmony(base_color, harmony_type)
        
        # Display generated colors
        color_display = Table(box=ROUNDED, expand=False)
        color_display.add_column("Index")
        color_display.add_column("Color")
        
        for i, color in enumerate(harmony_colors):
            color_display.add_row(str(i), color)
        
        self.console.print(Panel(color_display, title=f"{harmony_type.title()} Harmony", border_style="green"))
        
        # Option to apply colors to theme
        apply = Confirm.ask("Apply these colors to current theme?", default=False)
        if apply:
            # Apply main colors to theme
            if len(harmony_colors) >= 2:
                theme_creator.customize_color("background", harmony_colors[0])
                theme_creator.customize_color("accent", harmony_colors[1])
            if len(harmony_colors) >= 3:
                theme_creator.customize_color("border", harmony_colors[2])
            
            self.console.print("[bold green]Harmony colors applied to theme![/bold green]")
        
        time.sleep(3)

    def _show_gradient_theme_creator(self, theme_creator) -> None:
        """Show gradient theme creator interface."""
        self.clear()
        self.print_header("Gradient Theme Creator")
        self.console.print("[yellow]Gradient theme creator not yet implemented.[/yellow]")
        time.sleep(2)
    
    def _show_border_shape_options(self, theme_creator) -> None:
        """Show border and shape options interface."""
        self.clear()
        self.print_header("Border & Shape Options")
        self.console.print("[yellow]Border & shape options not yet implemented.[/yellow]")
        time.sleep(2)
    
    def _show_font_family_selection(self, theme_creator) -> None:
        """Show font family selection interface."""
        self.clear()
        self.print_header("Font Family Selection")
        self.console.print("[yellow]Font family selection not yet implemented.[/yellow]")
        time.sleep(2)
    
    def _load_theme_for_editing(self, theme_creator) -> None:
        """Load theme for editing interface."""
        self.clear()
        self.print_header("Load Theme for Editing")
        self.console.print("[yellow]Load theme for editing not yet implemented.[/yellow]")
        time.sleep(2)
    
    def _show_live_preview(self, theme_creator) -> None:
        """Show live preview interface."""
        self.clear()
        self.print_header("Live Preview")
        self.console.print("[yellow]Live preview not yet implemented.[/yellow]")
        time.sleep(2)

    def _save_custom_theme(self, theme_creator) -> bool:
        """Save custom theme interface."""
        self.clear()
        self.print_header("Save Custom Theme")
        
        theme_name = Prompt.ask("Enter theme name", default="My Custom Theme")
        description = Prompt.ask("Enter theme description (optional)", default="")
        
        success = theme_creator.save_custom_theme(theme_name, description)
        return success

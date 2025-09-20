"""
Helper methods for advanced footer/header customization UI.
Provides comprehensive controls for all text styling options.
"""

from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
import time
from typing import Dict, Any, List


class FooterUIHelpers:
    """
    Helper class containing UI methods for advanced footer/header customization.
    """
    
    def __init__(self, console, config_manager):
        """
        Initialize the footer UI helpers.
        
        Args:
            console: Rich console object
            config_manager: Configuration manager instance
        """
        self.console = console
        self.config_manager = config_manager
    
    def _edit_footer_basic_settings(self, config: Dict[str, Any]) -> None:
        """Edit basic footer settings (text, position, size, color)."""
        self.console.print("\n[bold cyan]Basic Footer Settings[/bold cyan]")
        
        # Enable/Disable
        config["enabled"] = Confirm.ask("Enable footer", default=config["enabled"])
        
        if config["enabled"]:
            # Text
            config["text"] = Prompt.ask("Footer text", default=config["text"])
            
            # Position options - enhanced with more choices
            positions = [
                "bottom", "bottom-left", "bottom-right", "bottom-center",
                "top", "top-left", "top-right", "top-center",
                "center", "center-left", "center-right"
            ]
            config["position"] = Prompt.ask("Position", choices=positions, default=config["position"])
            
            # Font size
            config["size"] = int(Prompt.ask("Font size (px)", default=str(config["size"])))
            
            # Color
            config["color"] = Prompt.ask("Text color (hex)", default=config["color"])
        
        self.console.print("[bold green]Basic settings updated![/bold green]")
        time.sleep(1)
    
    def _edit_footer_font_settings(self, config: Dict[str, Any]) -> None:
        """Edit font family and style settings."""
        self.console.print("\n[bold cyan]Font & Style Settings[/bold cyan]")
        
        # Font family options
        font_families = ["mono", "sans", "serif", "modern", "classic", "minimal"]
        current_family = config.get("font_family", "mono")
        config["font_family"] = Prompt.ask("Font family", choices=font_families, default=current_family)
        
        # Font style options
        font_styles = ["normal", "bold", "italic", "bold-italic"]
        current_style = config.get("font_style", "normal")
        config["font_style"] = Prompt.ask("Font style", choices=font_styles, default=current_style)
        
        self.console.print("[bold green]Font settings updated![/bold green]")
        time.sleep(1)
    
    def _edit_footer_effects(self, config: Dict[str, Any]) -> None:
        """Edit advanced effects (shadow, outline)."""
        self.console.print("\n[bold cyan]Advanced Effects[/bold cyan]")
        
        # Text shadow
        config["text_shadow"] = Confirm.ask("Enable text shadow", default=config.get("text_shadow", False))
        
        if config["text_shadow"]:
            config["shadow_color"] = Prompt.ask("Shadow color (hex)", default=config.get("shadow_color", "#FFFFFF"))
            
            # Shadow offset
            offset_x = int(Prompt.ask("Shadow offset X", default=str(config.get("shadow_offset", [2, 2])[0])))
            offset_y = int(Prompt.ask("Shadow offset Y", default=str(config.get("shadow_offset", [2, 2])[1])))
            config["shadow_offset"] = [offset_x, offset_y]
        
        # Text outline
        config["text_outline"] = Confirm.ask("Enable text outline", default=config.get("text_outline", False))
        
        if config["text_outline"]:
            config["outline_color"] = Prompt.ask("Outline color (hex)", default=config.get("outline_color", "#FFFFFF"))
            config["outline_width"] = int(Prompt.ask("Outline width (px)", default=str(config.get("outline_width", 1))))
        
        self.console.print("[bold green]Effects updated![/bold green]")
        time.sleep(1)
    
    def _edit_footer_background(self, config: Dict[str, Any]) -> None:
        """Edit background and border settings."""
        self.console.print("\n[bold cyan]Background & Border Settings[/bold cyan]")
        
        # Background
        config["background_enabled"] = Confirm.ask("Enable background", default=config.get("background_enabled", False))
        
        if config["background_enabled"]:
            config["background_color"] = Prompt.ask("Background color (hex)", default=config.get("background_color", "#000000"))
            config["background_opacity"] = int(Prompt.ask("Background opacity (0-255)", default=str(config.get("background_opacity", 128))))
            
            # Background padding
            pad_h = int(Prompt.ask("Horizontal padding", default=str(config.get("background_padding", [10, 5])[0])))
            pad_v = int(Prompt.ask("Vertical padding", default=str(config.get("background_padding", [10, 5])[1])))
            config["background_padding"] = [pad_h, pad_v]
            
            # Border
            config["background_border"] = Confirm.ask("Enable border", default=config.get("background_border", False))
            
            if config["background_border"]:
                config["border_color"] = Prompt.ask("Border color (hex)", default=config.get("border_color", "#FFFFFF"))
                config["border_width"] = int(Prompt.ask("Border width (px)", default=str(config.get("border_width", 1))))
        
        self.console.print("[bold green]Background settings updated![/bold green]")
        time.sleep(1)
    
    def _edit_footer_time_settings(self, config: Dict[str, Any]) -> None:
        """Edit time display settings."""
        self.console.print("\n[bold cyan]Time Display Settings[/bold cyan]")
        
        config["show_time"] = Confirm.ask("Show timestamp", default=config["show_time"])
        
        if config["show_time"]:
            # Time format presets
            format_presets = {
                "1": "%a %d.%b.%Y %H:%M",
                "2": "%Y-%m-%d %H:%M:%S",
                "3": "%d/%m/%Y %H:%M",
                "4": "%B %d, %Y at %I:%M %p",
                "5": "Custom"
            }
            
            self.console.print("\n[bold]Time Format Presets:[/bold]")
            for key, fmt in format_presets.items():
                if key != "5":
                    self.console.print(f"[{key}] {fmt}")
                else:
                    self.console.print(f"[{key}] {fmt}")
            
            choice = Prompt.ask("Choose format", choices=list(format_presets.keys()), default="1")
            
            if choice == "5":
                config["time_format"] = Prompt.ask("Custom format", default=config["time_format"])
            else:
                config["time_format"] = format_presets[choice]
            
            config["time_size"] = int(Prompt.ask("Time font size (px)", default=str(config["time_size"])))
        
        self.console.print("[bold green]Time settings updated![/bold green]")
        time.sleep(1)
    
    def _edit_footer_custom_elements(self, config: Dict[str, Any]) -> None:
        """Edit custom text elements."""
        self.console.print("\n[bold cyan]Custom Text Elements[/bold cyan]")
        
        # Ensure custom_elements exists
        if "custom_elements" not in config:
            config["custom_elements"] = []
        
        while True:
            # Show current elements
            elements = config["custom_elements"]
            
            if elements:
                table = Table(title="Current Custom Elements")
                table.add_column("Index", style="cyan")
                table.add_column("Text", style="green")
                table.add_column("Position", style="yellow")
                table.add_column("Enabled", style="magenta")
                
                for i, element in enumerate(elements):
                    table.add_row(
                        str(i + 1),
                        element.get("text", ""),
                        element.get("position", "center"),
                        "Yes" if element.get("enabled", True) else "No"
                    )
                
                self.console.print(table)
            else:
                self.console.print("[yellow]No custom elements defined.[/yellow]")
            
            # Menu
            self.console.print("\n[bold]Options:[/bold]")
            self.console.print("[a] Add new element")
            if elements:
                self.console.print("[e] Edit element")
                self.console.print("[d] Delete element")
                self.console.print("[t] Toggle element enabled/disabled")
            self.console.print("[b] Back")
            
            choice = Prompt.ask("Choose option", default="b")
            
            if choice == "a":
                self._add_custom_element(config)
            elif choice == "e" and elements:
                self._edit_custom_element(config)
            elif choice == "d" and elements:
                self._delete_custom_element(config)
            elif choice == "t" and elements:
                self._toggle_custom_element(config)
            elif choice == "b":
                break
        
        self.console.print("[bold green]Custom elements updated![/bold green]")
        time.sleep(1)
    
    def _add_custom_element(self, config: Dict[str, Any]) -> None:
        """Add a new custom text element."""
        element = {}
        
        element["text"] = Prompt.ask("Element text", default="Custom Text")
        
        positions = [
            "top-left", "top-center", "top-right",
            "center-left", "center", "center-right",
            "bottom-left", "bottom-center", "bottom-right"
        ]
        element["position"] = Prompt.ask("Position", choices=positions, default="center")
        
        element["size"] = int(Prompt.ask("Font size (px)", default="16"))
        element["color"] = Prompt.ask("Text color (hex)", default="#000000")
        
        # Font settings
        font_families = ["mono", "sans", "serif", "modern", "classic", "minimal"]
        element["font_family"] = Prompt.ask("Font family", choices=font_families, default="mono")
        
        font_styles = ["normal", "bold", "italic", "bold-italic"]
        element["font_style"] = Prompt.ask("Font style", choices=font_styles, default="normal")
        
        # Manual offset
        offset_x = int(Prompt.ask("X offset (px)", default="0"))
        offset_y = int(Prompt.ask("Y offset (px)", default="0"))
        element["offset"] = [offset_x, offset_y]
        
        element["enabled"] = True
        
        config["custom_elements"].append(element)
        self.console.print("[bold green]Custom element added![/bold green]")
        time.sleep(1)
    
    def _edit_custom_element(self, config: Dict[str, Any]) -> None:
        """Edit an existing custom element."""
        elements = config["custom_elements"]
        
        try:
            index = int(Prompt.ask(f"Element to edit (1-{len(elements)})")) - 1
            if 0 <= index < len(elements):
                element = elements[index]
                
                # Edit all properties
                element["text"] = Prompt.ask("Element text", default=element.get("text", ""))
                
                positions = [
                    "top-left", "top-center", "top-right",
                    "center-left", "center", "center-right", 
                    "bottom-left", "bottom-center", "bottom-right"
                ]
                element["position"] = Prompt.ask("Position", choices=positions, default=element.get("position", "center"))
                
                element["size"] = int(Prompt.ask("Font size (px)", default=str(element.get("size", 16))))
                element["color"] = Prompt.ask("Text color (hex)", default=element.get("color", "#000000"))
                
                self.console.print("[bold green]Element updated![/bold green]")
            else:
                self.console.print("[bold red]Invalid element index![/bold red]")
        except ValueError:
            self.console.print("[bold red]Invalid input![/bold red]")
        
        time.sleep(1)
    
    def _delete_custom_element(self, config: Dict[str, Any]) -> None:
        """Delete a custom element."""
        elements = config["custom_elements"]
        
        try:
            index = int(Prompt.ask(f"Element to delete (1-{len(elements)})")) - 1
            if 0 <= index < len(elements):
                element = elements[index]
                if Confirm.ask(f"Delete element '{element.get('text', '')}'?"):
                    del elements[index]
                    self.console.print("[bold green]Element deleted![/bold green]")
            else:
                self.console.print("[bold red]Invalid element index![/bold red]")
        except ValueError:
            self.console.print("[bold red]Invalid input![/bold red]")
        
        time.sleep(1)
    
    def _toggle_custom_element(self, config: Dict[str, Any]) -> None:
        """Toggle custom element enabled status."""
        elements = config["custom_elements"]
        
        try:
            index = int(Prompt.ask(f"Element to toggle (1-{len(elements)})")) - 1
            if 0 <= index < len(elements):
                element = elements[index]
                element["enabled"] = not element.get("enabled", True)
                status = "enabled" if element["enabled"] else "disabled"
                self.console.print(f"[bold green]Element {status}![/bold green]")
            else:
                self.console.print("[bold red]Invalid element index![/bold red]")
        except ValueError:
            self.console.print("[bold red]Invalid input![/bold red]")
        
        time.sleep(1)
    
    def _apply_footer_presets(self, config: Dict[str, Any]) -> None:
        """Apply predefined footer style presets."""
        self.console.print("\n[bold cyan]Footer Style Presets[/bold cyan]")
        
        presets = {
            "1": {
                "name": "Clean Minimal",
                "settings": {
                    "font_family": "minimal",
                    "font_style": "normal",
                    "text_shadow": False,
                    "text_outline": False,
                    "background_enabled": False,
                    "color": "#666666"
                }
            },
            "2": {
                "name": "Bold Modern",
                "settings": {
                    "font_family": "modern",
                    "font_style": "bold",
                    "text_shadow": True,
                    "shadow_color": "#FFFFFF",
                    "shadow_offset": [1, 1],
                    "text_outline": False,
                    "background_enabled": False,
                    "color": "#000000"
                }
            },
            "3": {
                "name": "Elegant Classic",
                "settings": {
                    "font_family": "classic",
                    "font_style": "italic",
                    "text_shadow": False,
                    "text_outline": True,
                    "outline_color": "#FFFFFF",
                    "outline_width": 1,
                    "background_enabled": False,
                    "color": "#333333"
                }
            },
            "4": {
                "name": "Gaming Style",
                "settings": {
                    "font_family": "modern",
                    "font_style": "bold",
                    "text_shadow": True,
                    "shadow_color": "#00FF00",
                    "shadow_offset": [2, 2],
                    "text_outline": True,
                    "outline_color": "#000000",
                    "outline_width": 1,
                    "background_enabled": True,
                    "background_color": "#000000",
                    "background_opacity": 180,
                    "color": "#00FF41"
                }
            },
            "5": {
                "name": "Professional",
                "settings": {
                    "font_family": "sans",
                    "font_style": "normal",
                    "text_shadow": False,
                    "text_outline": False,
                    "background_enabled": True,
                    "background_color": "#FFFFFF",
                    "background_opacity": 200,
                    "background_padding": [15, 8],
                    "background_border": True,
                    "border_color": "#CCCCCC",
                    "border_width": 1,
                    "color": "#333333"
                }
            }
        }
        
        # Show preset options
        for key, preset in presets.items():
            self.console.print(f"[{key}] {preset['name']}")
        
        choice = Prompt.ask("Choose preset", choices=list(presets.keys()) + ["b"], default="b")
        
        if choice != "b" and choice in presets:
            # Apply preset settings
            preset_settings = presets[choice]["settings"]
            for key, value in preset_settings.items():
                config[key] = value
            
            self.console.print(f"[bold green]Applied '{presets[choice]['name']}' preset![/bold green]")
        
        time.sleep(1)
    
    def _preview_footer_settings(self, config: Dict[str, Any]) -> None:
        """Preview current footer settings."""
        self.console.print("\n[bold cyan]Footer Preview[/bold cyan]")
        
        # Create a comprehensive settings display
        preview_panel = Panel(
            f"[bold]Text:[/bold] {config['text']}\n"
            f"[bold]Position:[/bold] {config['position']}\n"
            f"[bold]Font:[/bold] {config.get('font_family', 'mono')} {config.get('font_style', 'normal')}\n"
            f"[bold]Size:[/bold] {config['size']}px\n"
            f"[bold]Color:[/bold] {config['color']}\n\n"
            f"[bold]Effects:[/bold]\n"
            f"  Shadow: {'Yes' if config.get('text_shadow', False) else 'No'}\n"
            f"  Outline: {'Yes' if config.get('text_outline', False) else 'No'}\n\n"
            f"[bold]Background:[/bold]\n"
            f"  Enabled: {'Yes' if config.get('background_enabled', False) else 'No'}\n"
            f"  Color: {config.get('background_color', 'N/A')}\n"
            f"  Opacity: {config.get('background_opacity', 'N/A')}\n\n"
            f"[bold]Time Display:[/bold]\n"
            f"  Show: {'Yes' if config['show_time'] else 'No'}\n"
            f"  Format: {config['time_format']}\n"
            f"  Size: {config['time_size']}px\n\n"
            f"[bold]Custom Elements:[/bold] {len(config.get('custom_elements', []))}",
            title="Footer Configuration Preview",
            border_style="green"
        )
        
        self.console.print(preview_panel)
        
        input("\nPress Enter to continue...")
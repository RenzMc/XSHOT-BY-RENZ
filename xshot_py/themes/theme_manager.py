"""
Theme Manager for XShot

This module handles theme management and customization.
"""

from typing import Dict, Any, List, Optional, Tuple
import os
import yaml
import re
import colorsys
from pathlib import Path
from rich.style import Style
from rich.theme import Theme

class ThemeManager:
    """
    Manages themes for the XShot application.
    Handles loading built-in and custom themes.
    """
    
    # Built-in themes
    BUILT_IN_THEMES = {
        "dark": {
            "name": "Dark",
            "description": "Default dark theme",
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
        },
        "light": {
            "name": "Light",
            "description": "Clean light theme",
            "colors": {
                "background": "#F8F9FA",
                "foreground": "#1E222B",
                "accent": "#0078D7",
                "border": "#D1D5DB",
                "shadow": "#A1A1AA",
                "success": "#22C55E",
                "error": "#EF4444",
                "warning": "#F59E0B",
                "info": "#3B82F6",
                "muted": "#6B7280",
            },
            "ui": {
                "header_bg": "#F8F9FA",
                "header_fg": "#1E222B",
                "footer_bg": "#F8F9FA",
                "footer_fg": "#1E222B",
                "button_bg": "#E5E7EB",
                "button_fg": "#1E222B",
                "button_accent": "#0078D7",
                "input_bg": "#FFFFFF",
                "input_fg": "#1E222B",
                "panel_bg": "#FFFFFF",
                "panel_fg": "#1E222B",
            }
        },
        "nord": {
            "name": "Nord",
            "description": "Arctic-inspired theme",
            "colors": {
                "background": "#2E3440",
                "foreground": "#ECEFF4",
                "accent": "#88C0D0",
                "border": "#4C566A",
                "shadow": "#3B4252",
                "success": "#A3BE8C",
                "error": "#BF616A",
                "warning": "#EBCB8B",
                "info": "#81A1C1",
                "muted": "#D8DEE9",
            },
            "ui": {
                "header_bg": "#2E3440",
                "header_fg": "#ECEFF4",
                "footer_bg": "#2E3440",
                "footer_fg": "#ECEFF4",
                "button_bg": "#4C566A",
                "button_fg": "#ECEFF4",
                "button_accent": "#88C0D0",
                "input_bg": "#3B4252",
                "input_fg": "#ECEFF4",
                "panel_bg": "#3B4252",
                "panel_fg": "#ECEFF4",
            }
        },
        "dracula": {
            "name": "Dracula",
            "description": "Dark theme with vibrant colors",
            "colors": {
                "background": "#282A36",
                "foreground": "#F8F8F2",
                "accent": "#BD93F9",
                "border": "#44475A",
                "shadow": "#191A21",
                "success": "#50FA7B",
                "error": "#FF5555",
                "warning": "#FFB86C",
                "info": "#8BE9FD",
                "muted": "#BFBFBF",
            },
            "ui": {
                "header_bg": "#282A36",
                "header_fg": "#F8F8F2",
                "footer_bg": "#282A36",
                "footer_fg": "#F8F8F2",
                "button_bg": "#44475A",
                "button_fg": "#F8F8F2",
                "button_accent": "#BD93F9",
                "input_bg": "#383A59",
                "input_fg": "#F8F8F2",
                "panel_bg": "#383A59",
                "panel_fg": "#F8F8F2",
            }
        }
    }
    
    def __init__(self, themes_dir: Optional[str] = None):
        """
        Initialize the theme manager.
        
        Args:
            themes_dir: Directory to store custom themes. If None, uses ~/.config/xshot/themes
        """
        if themes_dir is None:
            self.themes_dir = os.path.expanduser("~/.config/xshot/themes")
        else:
            self.themes_dir = os.path.expanduser(themes_dir)
            
        # Ensure themes directory exists
        os.makedirs(self.themes_dir, exist_ok=True)
        
        # Load custom themes
        self.custom_themes = self._load_custom_themes()
        
    def _load_custom_themes(self) -> Dict[str, Dict[str, Any]]:
        """
        Load custom themes from the themes directory.
        
        Returns:
            Dictionary of custom themes
        """
        custom_themes = {}
        
        for file_path in Path(self.themes_dir).glob("*.yaml"):
            try:
                with open(file_path, 'r') as f:
                    theme_data = yaml.safe_load(f)
                
                theme_id = file_path.stem
                if self._validate_theme(theme_data):
                    custom_themes[theme_id] = theme_data
            except Exception as e:
                print(f"Error loading theme {file_path}: {e}")
                
        return custom_themes
    
    def _validate_theme(self, theme_data: Dict[str, Any]) -> bool:
        """
        Validate theme data structure.
        
        Args:
            theme_data: Theme data to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_sections = ["name", "colors", "ui"]
        required_colors = ["background", "foreground", "accent", "border"]
        required_ui = ["header_bg", "header_fg", "button_bg", "button_fg"]
        
        # Check required sections
        for section in required_sections:
            if section not in theme_data:
                return False
        
        # Check required colors
        for color in required_colors:
            if color not in theme_data["colors"]:
                return False
                
        # Check required UI elements
        for ui_elem in required_ui:
            if ui_elem not in theme_data["ui"]:
                return False
                
        return True
    
    def get_theme_list(self) -> List[Dict[str, str]]:
        """
        Get a list of all available themes.
        
        Returns:
            List of theme information dictionaries
        """
        themes = []
        
        # Add built-in themes
        for theme_id, theme_data in self.BUILT_IN_THEMES.items():
            themes.append({
                "id": theme_id,
                "name": theme_data["name"],
                "description": theme_data["description"],
                "type": "built-in"
            })
            
        # Add custom themes
        for theme_id, theme_data in self.custom_themes.items():
            themes.append({
                "id": theme_id,
                "name": theme_data["name"],
                "description": theme_data.get("description", "Custom theme"),
                "type": "custom"
            })
            
        return themes
    
    def get_theme(self, theme_id: str) -> Dict[str, Any]:
        """
        Get a theme by ID.
        
        Args:
            theme_id: Theme identifier
            
        Returns:
            Theme data dictionary or None if not found
        """
        if theme_id in self.BUILT_IN_THEMES:
            return self.BUILT_IN_THEMES[theme_id]
        elif theme_id in self.custom_themes:
            return self.custom_themes[theme_id]
        else:
            # Return default theme if not found
            return self.BUILT_IN_THEMES["dark"]
    
    def create_rich_theme(self, theme_id: str) -> Theme:
        """
        Create a Rich Theme object from a theme ID.
        
        Args:
            theme_id: Theme identifier
            
        Returns:
            Rich Theme object
        """
        theme_data = self.get_theme(theme_id)
        
        # Create styles dictionary for Rich Theme
        styles = {
            "header": Style(color=theme_data["ui"]["header_fg"], bgcolor=theme_data["ui"]["header_bg"]),
            "footer": Style(color=theme_data["ui"]["footer_fg"], bgcolor=theme_data["ui"]["footer_bg"]),
            "button": Style(color=theme_data["ui"]["button_fg"], bgcolor=theme_data["ui"]["button_bg"]),
            "button.accent": Style(color=theme_data["ui"]["button_fg"], bgcolor=theme_data["ui"]["button_accent"]),
            "input": Style(color=theme_data["ui"]["input_fg"], bgcolor=theme_data["ui"]["input_bg"]),
            "panel": Style(color=theme_data["ui"]["panel_fg"], bgcolor=theme_data["ui"]["panel_bg"]),
            "success": Style(color=theme_data["colors"]["success"]),
            "error": Style(color=theme_data["colors"]["error"]),
            "warning": Style(color=theme_data["colors"]["warning"]),
            "info": Style(color=theme_data["colors"]["info"]),
            "muted": Style(color=theme_data["colors"]["muted"]),
        }
        
        return Theme(styles)
    
    def save_custom_theme(self, theme_id: str, theme_data: Dict[str, Any]) -> bool:
        """
        Save a custom theme.
        
        Args:
            theme_id: Theme identifier
            theme_data: Theme data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not self._validate_theme(theme_data):
            return False
            
        try:
            file_path = os.path.join(self.themes_dir, f"{theme_id}.yaml")
            with open(file_path, 'w') as f:
                yaml.dump(theme_data, f, default_flow_style=False)
                
            # Update custom themes
            self.custom_themes[theme_id] = theme_data
            return True
        except Exception as e:
            print(f"Error saving theme: {e}")
            return False
    
    def delete_custom_theme(self, theme_id: str) -> bool:
        """
        Delete a custom theme.
        
        Args:
            theme_id: Theme identifier
            
        Returns:
            True if successful, False otherwise
        """
        if theme_id in self.custom_themes:
            try:
                file_path = os.path.join(self.themes_dir, f"{theme_id}.yaml")
                os.remove(file_path)
                
                # Remove from custom themes
                del self.custom_themes[theme_id]
                return True
            except Exception as e:
                print(f"Error deleting theme: {e}")
                return False
        return False


class CustomThemeCreator:
    """
    Advanced theme creator with UI-based customization capabilities.
    Provides color pickers, shape options, and real-time preview.
    """
    
    def __init__(self, theme_manager: 'ThemeManager'):
        """
        Initialize the custom theme creator.
        
        Args:
            theme_manager: Reference to the main theme manager
        """
        self.theme_manager = theme_manager
        self.current_theme = self._get_base_template()
        self.preview_mode = False
        
        # Color palette presets for easy selection
        self.color_palettes = {
            "Material Design": {
                "primary": "#2196F3",
                "primary_dark": "#1976D2", 
                "accent": "#FF4081",
                "background": "#FAFAFA",
                "surface": "#FFFFFF",
                "text": "#212121",
                "text_secondary": "#757575"
            },
            "Nord": {
                "primary": "#5E81AC",
                "primary_dark": "#2E3440",
                "accent": "#88C0D0", 
                "background": "#ECEFF4",
                "surface": "#E5E9F0",
                "text": "#2E3440",
                "text_secondary": "#4C566A"
            },
            "Dracula": {
                "primary": "#BD93F9",
                "primary_dark": "#6272A4",
                "accent": "#50FA7B",
                "background": "#282A36",
                "surface": "#44475A",
                "text": "#F8F8F2",
                "text_secondary": "#6272A4"
            },
            "Cyberpunk": {
                "primary": "#00F5FF",
                "primary_dark": "#001F3F",
                "accent": "#FF073A",
                "background": "#0A0A0A",
                "surface": "#1A1A1A",
                "text": "#00F5FF",
                "text_secondary": "#7FDBFF"
            },
            "Sunset": {
                "primary": "#FF6B35",
                "primary_dark": "#D62828",
                "accent": "#FFD23F",
                "background": "#FFF8DC",
                "surface": "#FFEAA7",
                "text": "#2D3436",
                "text_secondary": "#636E72"
            }
        }
        
        # Shape and border options
        self.border_styles = {
            "rounded": {"radius": 15, "style": "smooth"},
            "sharp": {"radius": 0, "style": "sharp"},
            "pill": {"radius": 50, "style": "pill"},
            "custom": {"radius": 10, "style": "custom"}
        }
        
        # Font options for different elements
        self.font_options = {
            "modern": {
                "main": "DejaVuSans.ttf",
                "mono": "JetBrains Mono Medium Nerd Font Complete.ttf",
                "display": "DejaVuSans-Bold.ttf"
            },
            "classic": {
                "main": "DejaVuSerif.ttf", 
                "mono": "DejaVuSansMono.ttf",
                "display": "DejaVuSerif-Bold.ttf"
            },
            "minimal": {
                "main": "DejaVuSans-ExtraLight.ttf",
                "mono": "DejaVuSansMono.ttf", 
                "display": "DejaVuSans.ttf"
            }
        }
    
    def _get_base_template(self) -> Dict[str, Any]:
        """
        Get a base theme template for customization.
        
        Returns:
            Base theme template
        """
        return {
            "name": "Custom Theme",
            "description": "User-created custom theme",
            "colors": {
                "background": "#2E3440",
                "foreground": "#ECEFF4", 
                "accent": "#88C0D0",
                "border": "#4C566A",
                "shadow": "#3B4252",
                "success": "#A3BE8C",
                "error": "#BF616A",
                "warning": "#EBCB8B",
                "info": "#81A1C1",
                "muted": "#D8DEE9",
            },
            "ui": {
                "header_bg": "#2E3440",
                "header_fg": "#ECEFF4",
                "footer_bg": "#2E3440", 
                "footer_fg": "#ECEFF4",
                "button_bg": "#4C566A",
                "button_fg": "#ECEFF4",
                "button_accent": "#88C0D0",
                "input_bg": "#3B4252",
                "input_fg": "#ECEFF4",
                "panel_bg": "#3B4252",
                "panel_fg": "#ECEFF4",
            },
            "advanced": {
                "border_style": "rounded",
                "border_width": 2,
                "shadow_style": "soft",
                "shadow_opacity": 0.3,
                "gradient_enabled": False,
                "gradient_direction": "vertical",
                "animation_speed": "normal",
                "font_family": "modern"
            }
        }
    
    def apply_color_palette(self, palette_name: str) -> bool:
        """
        Apply a predefined color palette to the current theme.
        
        Args:
            palette_name: Name of the color palette
            
        Returns:
            True if successful, False otherwise
        """
        if palette_name not in self.color_palettes:
            return False
        
        palette = self.color_palettes[palette_name]
        
        # Map palette colors to theme structure
        self.current_theme["colors"].update({
            "background": palette["background"],
            "foreground": palette["text"],
            "accent": palette["accent"],
            "border": self._darken_color(palette["surface"], 0.2),
            "shadow": self._darken_color(palette["background"], 0.4)
        })
        
        self.current_theme["ui"].update({
            "header_bg": palette["primary"],
            "header_fg": palette["text"] if self._is_light_color(palette["primary"]) else "#FFFFFF",
            "footer_bg": palette["primary_dark"],
            "footer_fg": "#FFFFFF",
            "button_bg": palette["surface"],
            "button_fg": palette["text"],
            "button_accent": palette["accent"]
        })
        
        return True
    
    def customize_color(self, element: str, color: str, section: str = "colors") -> bool:
        """
        Customize a specific color element.
        
        Args:
            element: Color element name
            color: New color value (hex, rgb, etc.)
            section: Theme section ("colors" or "ui")
            
        Returns:
            True if successful, False otherwise
        """
        if not self._validate_color(color):
            return False
        
        if section not in self.current_theme:
            return False
        
        if element not in self.current_theme[section]:
            return False
        
        # Normalize color format
        normalized_color = self._normalize_color(color)
        self.current_theme[section][element] = normalized_color
        
        # Auto-adjust related colors for better harmony
        self._auto_adjust_related_colors(element, normalized_color, section)
        
        return True
    
    def generate_color_harmony(self, base_color: str, harmony_type: str = "complementary") -> List[str]:
        """
        Generate color harmony based on a base color.
        
        Args:
            base_color: Base color in hex format
            harmony_type: Type of harmony ("complementary", "triadic", "analogous", "monochromatic")
            
        Returns:
            List of harmonious colors
        """
        if not self._validate_color(base_color):
            return [base_color]
        
        # Convert hex to HSV
        h, s, v = self._hex_to_hsv(base_color)
        colors = [base_color]
        
        if harmony_type == "complementary":
            # Complementary color (180 degrees)
            comp_h = (h + 0.5) % 1.0
            colors.append(self._hsv_to_hex(comp_h, s, v))
            
        elif harmony_type == "triadic":
            # Triadic colors (120 degrees apart)
            for offset in [1/3, 2/3]:
                new_h = (h + offset) % 1.0
                colors.append(self._hsv_to_hex(new_h, s, v))
                
        elif harmony_type == "analogous":
            # Analogous colors (30 degrees apart)
            for offset in [-1/12, 1/12, -2/12, 2/12]:
                new_h = (h + offset) % 1.0
                colors.append(self._hsv_to_hex(new_h, s, v))
                
        elif harmony_type == "monochromatic":
            # Monochromatic variations (different saturation/value)
            for s_var, v_var in [(s*0.5, v), (s, v*0.7), (s*0.8, v*1.2), (s*1.2, v*0.8)]:
                s_var = min(1.0, max(0.0, s_var))
                v_var = min(1.0, max(0.0, v_var))
                colors.append(self._hsv_to_hex(h, s_var, v_var))
        
        return colors
    
    def create_gradient_theme(self, start_color: str, end_color: str, steps: int = 5) -> Dict[str, str]:
        """
        Create a gradient-based color scheme.
        
        Args:
            start_color: Starting color
            end_color: Ending color
            steps: Number of gradient steps
            
        Returns:
            Dictionary of gradient colors
        """
        if not (self._validate_color(start_color) and self._validate_color(end_color)):
            return {}
        
        start_rgb = self._hex_to_rgb(start_color)
        end_rgb = self._hex_to_rgb(end_color)
        
        gradient_colors = {}
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            
            gradient_colors[f"gradient_{i}"] = f"#{r:02x}{g:02x}{b:02x}"
        
        return gradient_colors
    
    def apply_border_style(self, style_name: str, custom_radius: Optional[int] = None) -> bool:
        """
        Apply a border style to the current theme.
        
        Args:
            style_name: Border style name
            custom_radius: Custom radius for "custom" style
            
        Returns:
            True if successful, False otherwise
        """
        if style_name not in self.border_styles and style_name != "custom":
            return False
        
        if style_name == "custom" and custom_radius is not None:
            self.current_theme["advanced"]["border_style"] = "custom"
            self.current_theme["advanced"]["border_radius"] = custom_radius
        else:
            style = self.border_styles[style_name]
            self.current_theme["advanced"]["border_style"] = style_name
            self.current_theme["advanced"]["border_radius"] = style["radius"]
        
        return True
    
    def apply_font_family(self, family_name: str) -> bool:
        """
        Apply a font family to the current theme.
        
        Args:
            family_name: Font family name
            
        Returns:
            True if successful, False otherwise
        """
        if family_name not in self.font_options:
            return False
        
        self.current_theme["advanced"]["font_family"] = family_name
        return True
    
    def get_theme_preview(self) -> Dict[str, Any]:
        """
        Get a preview of the current theme with sample elements.
        
        Returns:
            Preview data for the theme
        """
        return {
            "theme_data": self.current_theme.copy(),
            "preview_elements": {
                "header": {
                    "background": self.current_theme["ui"]["header_bg"],
                    "text": self.current_theme["ui"]["header_fg"],
                    "sample_text": "XShot Theme Preview"
                },
                "button": {
                    "background": self.current_theme["ui"]["button_bg"],
                    "text": self.current_theme["ui"]["button_fg"],
                    "accent": self.current_theme["ui"]["button_accent"],
                    "sample_text": "Sample Button"
                },
                "panel": {
                    "background": self.current_theme["ui"]["panel_bg"],
                    "text": self.current_theme["ui"]["panel_fg"],
                    "border": self.current_theme["colors"]["border"],
                    "sample_text": "This is a preview panel with the selected theme colors."
                }
            }
        }
    
    def save_custom_theme(self, theme_name: str, description: str = "") -> bool:
        """
        Save the current custom theme.
        
        Args:
            theme_name: Name for the custom theme
            description: Description of the theme
            
        Returns:
            True if successful, False otherwise
        """
        if not theme_name or not theme_name.strip():
            return False
        
        # Update theme metadata
        self.current_theme["name"] = theme_name.strip()
        self.current_theme["description"] = description.strip() or f"Custom theme: {theme_name}"
        
        # Generate unique theme ID
        theme_id = self._generate_theme_id(theme_name)
        
        # Save using the theme manager
        return self.theme_manager.save_custom_theme(theme_id, self.current_theme)
    
    def load_theme_for_editing(self, theme_id: str) -> bool:
        """
        Load an existing theme for editing.
        
        Args:
            theme_id: Theme identifier
            
        Returns:
            True if successful, False otherwise
        """
        theme_data = self.theme_manager.get_theme(theme_id)
        if not theme_data:
            return False
        
        self.current_theme = theme_data.copy()
        
        # Ensure advanced settings exist
        if "advanced" not in self.current_theme:
            self.current_theme["advanced"] = self._get_base_template()["advanced"]
        
        return True
    
    def reset_theme(self) -> None:
        """Reset the current theme to the base template."""
        self.current_theme = self._get_base_template()
    
    # Helper methods for color manipulation
    def _validate_color(self, color: str) -> bool:
        """Validate if a color string is valid."""
        if not color:
            return False
        
        # Check hex format
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        if re.match(hex_pattern, color):
            return True
        
        # Check rgb format
        rgb_pattern = r'^rgb\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
        if re.match(rgb_pattern, color):
            return True
        
        return False
    
    def _normalize_color(self, color: str) -> str:
        """Normalize color to hex format."""
        if color.startswith('#'):
            return color.upper()
        
        if color.startswith('rgb'):
            # Extract RGB values
            rgb_values = re.findall(r'\d+', color)
            if len(rgb_values) == 3:
                r, g, b = map(int, rgb_values)
                return f"#{r:02X}{g:02X}{b:02X}"
        
        return color
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB values to hex color."""
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def _hex_to_hsv(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to HSV."""
        r, g, b = self._hex_to_rgb(hex_color)
        return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    def _hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """Convert HSV to hex color."""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return self._rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def _is_light_color(self, hex_color: str) -> bool:
        """Check if a color is light or dark."""
        r, g, b = self._hex_to_rgb(hex_color)
        # Calculate perceived lightness
        lightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return lightness > 0.5
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        """Darken a color by a given factor."""
        h, s, v = self._hex_to_hsv(hex_color)
        v = max(0, v - factor)
        return self._hsv_to_hex(h, s, v)
    
    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Lighten a color by a given factor."""
        h, s, v = self._hex_to_hsv(hex_color)
        v = min(1, v + factor)
        return self._hsv_to_hex(h, s, v)
    
    def _auto_adjust_related_colors(self, element: str, color: str, section: str) -> None:
        """Auto-adjust related colors for better harmony."""
        if section == "colors" and element == "background":
            # Adjust foreground for contrast
            if self._is_light_color(color):
                self.current_theme["colors"]["foreground"] = "#2E3440"
            else:
                self.current_theme["colors"]["foreground"] = "#ECEFF4"
        
        elif section == "ui" and element == "header_bg":
            # Adjust header text for contrast
            if self._is_light_color(color):
                self.current_theme["ui"]["header_fg"] = "#2E3440"
            else:
                self.current_theme["ui"]["header_fg"] = "#ECEFF4"
    
    def _generate_theme_id(self, theme_name: str) -> str:
        """Generate a unique theme ID from theme name."""
        # Convert to lowercase and replace spaces with underscores
        theme_id = theme_name.lower().replace(' ', '_')
        # Remove special characters
        theme_id = re.sub(r'[^a-z0-9_]', '', theme_id)
        
        # Ensure uniqueness
        counter = 1
        original_id = theme_id
        while theme_id in self.theme_manager.custom_themes:
            theme_id = f"{original_id}_{counter}"
            counter += 1
        
        return theme_id
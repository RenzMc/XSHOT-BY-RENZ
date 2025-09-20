"""
Configuration Manager for XShot

This module handles loading, saving, and managing user configurations.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Manages configuration settings for XShot application.
    Handles loading from and saving to YAML files.
    """
    
    DEFAULT_CONFIG = {
        "general": {
            "screenshot_dir": "~/Pictures/Screenshots",
            "output_dir": "~/Pictures/XShot",
            "backup_dir": "~/Pictures/XShot/Backups",
            "auto_open": True,
            "auto_backup": True,
        },
        "appearance": {
            "theme": "dark",
            "custom_theme": None,
        },
        "border": {
            "size": 50,
            "radius": 10,
            "color_dark": "#3d465c",
            "color_light": "#F8F9FA",
            "shadow_size": "85x10+0+10",
            "shadow_color": "#000000",
        },
        "titlebar": {
            "enabled": True,
            "size": 20,
            "show_device_info": True,
            "custom_text": None,
        },
        "footer": {
            "enabled": True,
            "text": "Shot by XShot",
            "position": "bottom",
            "size": 20,
            "color": "#000000",
            "show_time": True,
            "time_format": "%a %d.%b.%Y %H:%M",
            "time_size": 15,
            # Enhanced customization options
            "font_family": "mono",  # mono, sans, serif, modern, classic, minimal
            "font_style": "normal",  # normal, bold, italic, bold-italic
            "text_shadow": False,
            "shadow_color": "#FFFFFF",
            "shadow_offset": [2, 2],
            "text_outline": False,
            "outline_color": "#FFFFFF",
            "outline_width": 1,
            "background_enabled": False,
            "background_color": "#000000",
            "background_opacity": 128,  # 0-255
            "background_padding": [10, 5],  # [horizontal, vertical]
            "background_border": False,
            "border_color": "#FFFFFF",
            "border_width": 1,
            "custom_elements": [],  # List of additional custom text elements
        },
        "header": {
            "enabled": False,
            "text": "XShot Screenshot",
            "position": "top",
            "size": 22,
            "color": "#000000",
            "show_time": False,
            "time_format": "%a %d.%b.%Y %H:%M",
            "time_size": 18,
            # Enhanced customization options (same as footer)
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
            "custom_elements": [],
        },
        "custom_image": {
            "enabled": False,
            "path": None,
            "position": "bottom-left",  # Options: top-left, top-right, bottom-left, bottom-right
            "size": 100,  # Size in pixels
            "padding": 10,  # Padding from the edge
        },
        "auto_detection": {
            "enabled": False,
            "watch_dirs": ["~/Pictures/Screenshots"],
            "file_patterns": ["*.png", "*.jpg", "*.jpeg"],
        },
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory to store configuration files. If None, uses ~/.config/xshot
        """
        if config_dir is None:
            self.config_dir = os.path.expanduser("~/.config/xshot")
        else:
            self.config_dir = os.path.expanduser(config_dir)
            
        self.config_file = os.path.join(self.config_dir, "config.yaml")
        self.config = None
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load or create default config
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default if not exists.
        
        Returns:
            Dict containing configuration settings
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f)
                
                # Update with any missing default values
                self._update_with_defaults(self.config, self.DEFAULT_CONFIG)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = self.DEFAULT_CONFIG.copy()
        else:
            self.config = self.DEFAULT_CONFIG.copy()
            self.save_config()
            
        return self.config
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value with enhanced safety.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        if self.config is None:
            return default
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default
    
    def get_section(self, section: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get an entire configuration section safely.
        
        Args:
            section: Configuration section name
            default: Default value if section not found
            
        Returns:
            Configuration section or default
        """
        if self.config is None:
            return default or {}
        return self.config.get(section, default or {})
    
    def safe_get_nested(self, path: str, default: Any = None) -> Any:
        """
        Safely get nested configuration values using dot notation.
        
        Args:
            path: Dot-separated path (e.g., 'general.output_dir')
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        if self.config is None:
            return default
            
        keys = path.split('.')
        current = self.config
        
        try:
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default
            return current
        except (TypeError, AttributeError):
            return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
    
    def _update_with_defaults(self, config: Dict[str, Any], defaults: Dict[str, Any]) -> None:
        """
        Update config with any missing default values recursively.
        
        Args:
            config: Current configuration
            defaults: Default configuration
        """
        for section, values in defaults.items():
            if section not in config:
                config[section] = values.copy()
            elif isinstance(values, dict):
                for key, value in values.items():
                    if key not in config[section]:
                        config[section][key] = value
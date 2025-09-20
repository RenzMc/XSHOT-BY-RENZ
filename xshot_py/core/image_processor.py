"""
Image Processor for XShot

This module handles all image processing operations for enhancing screenshots.
"""

import os
import sys
import time
import shutil
import platform
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, Union
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
except ImportError:
    print("Error: Pillow library not found. Please install it using: pip install Pillow")
    sys.exit(1)

from .text_renderer import TextRenderer

class ImageProcessor:
    """
    Handles image processing operations for XShot.
    """
    
    def __init__(self, config: Dict[str, Any], theme_data: Dict[str, Any]):
        """
        Initialize the image processor.
        
        Args:
            config: Application configuration
            theme_data: Current theme data
        """
        self.config = config
        self.theme_data = theme_data
        
        # Enhanced cross-platform font directory detection
        self.fonts_dir = self._get_fonts_directory()
        
        # Fallback system fonts for different platforms
        self.system_fonts = self._get_system_fonts()
        
        # Cross-platform directory creation with enhanced error handling
        self._ensure_directories_exist()
        
        # Initialize the advanced text renderer
        self.text_renderer = TextRenderer(config)
    
    def _get_fonts_directory(self) -> str:
        """
        Get fonts directory with enhanced cross-platform support.
        
        Returns:
            Path to fonts directory
        """
        try:
            # Method 1: Try package structure first
            import xshot_py
            package_dir = os.path.dirname(os.path.dirname(xshot_py.__file__))
            fonts_dir = os.path.join(package_dir, "xshot_py", "assets", "fonts")
            if os.path.exists(fonts_dir):
                return fonts_dir
        except ImportError:
            pass
        
        # Method 2: Try relative to current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(current_dir, "..", "assets", "fonts")
        fonts_dir = os.path.abspath(fonts_dir)
        if os.path.exists(fonts_dir):
            return fonts_dir
        
        # Method 3: Try relative to main file location
        fonts_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
        fonts_dir = os.path.abspath(fonts_dir)
        if os.path.exists(fonts_dir):
            return fonts_dir
        
        # Method 4: Create a default fonts directory in user config
        config_dir = os.path.expanduser("~/.config/xshot/fonts")
        os.makedirs(config_dir, exist_ok=True)
        return config_dir
    
    def _get_system_fonts(self) -> Dict[str, Optional[str]]:
        """
        Get system fonts for different platforms as fallbacks.
        
        Returns:
            Dictionary of font paths for different purposes
        """
        system = platform.system().lower()
        fonts = {
            "default": None,
            "mono": None,
            "bold": None
        }
        
        try:
            if system == "windows":
                fonts["default"] = "C:/Windows/Fonts/arial.ttf"
                fonts["mono"] = "C:/Windows/Fonts/consola.ttf"
                fonts["bold"] = "C:/Windows/Fonts/arialbd.ttf"
            elif system == "darwin":  # macOS
                fonts["default"] = "/System/Library/Fonts/Helvetica.ttc"
                fonts["mono"] = "/System/Library/Fonts/Monaco.ttf"
                fonts["bold"] = "/System/Library/Fonts/HelveticaNeue.ttc"
            else:  # Linux and others
                # Common Linux font paths
                common_paths = [
                    "/usr/share/fonts",
                    "/usr/local/share/fonts",
                    "~/.fonts",
                    "~/.local/share/fonts"
                ]
                
                # Look for common fonts
                for base_path in common_paths:
                    base_path = os.path.expanduser(base_path)
                    if os.path.exists(base_path):
                        # Try to find DejaVu fonts (very common on Linux)
                        dejavu_path = self._find_font_in_directory(base_path, "DejaVuSans.ttf")
                        if dejavu_path:
                            fonts["default"] = dejavu_path
                        
                        dejavu_mono_path = self._find_font_in_directory(base_path, "DejaVuSansMono.ttf")
                        if dejavu_mono_path:
                            fonts["mono"] = dejavu_mono_path
                        
                        dejavu_bold_path = self._find_font_in_directory(base_path, "DejaVuSans-Bold.ttf")
                        if dejavu_bold_path:
                            fonts["bold"] = dejavu_bold_path
                            
                        if fonts["default"] and fonts["mono"]:
                            break
        except Exception as e:
            print(f"Warning: Error detecting system fonts: {e}")
        
        return fonts
    
    def _load_font(self, font_type: str = "default", size: int = 20) -> ImageFont.FreeTypeFont:
        """
        Load a font with enhanced cross-platform fallback support.
        
        Args:
            font_type: Type of font ("default", "mono", "bold")
            size: Font size
            
        Returns:
            PIL ImageFont object
        """
        font_paths_to_try = []
        
        # Try bundled fonts first
        bundled_fonts = {
            "default": "DejaVuSans.ttf",
            "mono": "JetBrains Mono Medium Nerd Font Complete.ttf",
            "bold": "DejaVuSans-Bold.ttf"
        }
        
        if font_type in bundled_fonts:
            bundled_path = os.path.join(self.fonts_dir, bundled_fonts[font_type])
            font_paths_to_try.append(bundled_path)
            
            # Also try alternative names
            if font_type == "mono":
                font_paths_to_try.extend([
                    os.path.join(self.fonts_dir, "DejaVuSansMono.ttf"),
                    os.path.join(self.fonts_dir, "JetBrains Mono Bold Nerd Font Complete.ttf")
                ])
        
        # Try system fonts
        if font_type in self.system_fonts and self.system_fonts[font_type]:
            font_paths_to_try.append(self.system_fonts[font_type])
        
        # Try loading each font path
        for font_path in font_paths_to_try:
            try:
                if font_path and os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            except Exception as e:
                print(f"Warning: Could not load font {font_path}: {e}")
                continue
        
        # Ultimate fallback: try to load any available font
        try:
            # Try default PIL font with size
            return ImageFont.load_default()
        except Exception:
            # If even that fails, create a minimal font
            return ImageFont.load_default()
    
    def _check_text_bounds(self, x: int, y: int, text: str, font: ImageFont.FreeTypeFont, 
                          img_width: int, img_height: int, padding: int = 20) -> Tuple[int, int]:
        """
        Check and adjust text position to ensure it stays within image bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate  
            text: Text to be drawn
            font: Font object
            img_width: Image width
            img_height: Image height
            padding: Minimum padding from edges
            
        Returns:
            Adjusted (x, y) coordinates
        """
        try:
            # Create a temporary draw object to measure text
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            
            # Get text dimensions
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Adjust X coordinate if text goes beyond right edge
            if x + text_width > img_width - padding:
                x = max(padding, img_width - text_width - padding)
            
            # Ensure X is not negative
            if x < padding:
                x = padding
            
            # Adjust Y coordinate if text goes beyond bottom edge
            if y + text_height > img_height - padding:
                y = max(padding, img_height - text_height - padding)
            
            # Ensure Y is not negative
            if y < padding:
                y = padding
                
        except Exception as e:
            print(f"Warning: Error checking text bounds: {e}")
            # Return original coordinates if bounds checking fails
            pass
        
        return int(x), int(y)
    
    def _find_font_in_directory(self, directory: str, font_name: str) -> Optional[str]:
        """
        Recursively find a font file in a directory.
        
        Args:
            directory: Directory to search
            font_name: Font filename to find
            
        Returns:
            Full path to font file or None if not found
        """
        try:
            for root, dirs, files in os.walk(directory):
                if font_name in files:
                    return os.path.join(root, font_name)
        except Exception:
            pass
        return None
    
    def _ensure_directories_exist(self) -> None:
        """
        Ensure all required directories exist with enhanced error handling.
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.expanduser(self.config["general"]["output_dir"])
            os.makedirs(output_dir, exist_ok=True)
            
            # Ensure backup directory exists if auto_backup is enabled
            if self.config["general"]["auto_backup"]:
                backup_dir = os.path.expanduser(self.config["general"]["backup_dir"])
                os.makedirs(backup_dir, exist_ok=True)
                
            # Ensure fonts directory exists
            os.makedirs(self.fonts_dir, exist_ok=True)
            
        except Exception as e:
            print(f"Warning: Error creating directories: {e}")
            # Create fallback directories in current working directory
            try:
                fallback_output = os.path.join(os.getcwd(), "xshot_output")
                os.makedirs(fallback_output, exist_ok=True)
                self.config["general"]["output_dir"] = fallback_output
                print(f"Using fallback output directory: {fallback_output}")
            except Exception as fallback_error:
                print(f"Error creating fallback directories: {fallback_error}")
    
    def process_image(self, image_path: str) -> str:
        """
        Process an image with the current configuration.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Path to the processed image
        """
        # Create backup if enabled
        if self.config["general"]["auto_backup"]:
            self._backup_image(image_path)
        
        # Open the image
        try:
            img = Image.open(image_path)
            
            # Convert RGB to RGBA for transparency support
            if img.mode == 'RGB':
                img = img.convert('RGBA')
        except Exception as e:
            print(f"Error opening image: {e}")
            return image_path
        
        # Add titlebar if enabled
        if self.config["titlebar"]["enabled"]:
            img = self._add_titlebar(img)
        
        # Add border and shadow
        img = self._add_border_and_shadow(img)
        
        # Add footer if enabled
        if self.config["footer"]["enabled"]:
            img = self._add_footer(img)
        
        # Add custom image if enabled
        if self.config["custom_image"]["enabled"] and self.config["custom_image"]["path"]:
            img = self._add_custom_image(img)
        
        # Save the processed image
        output_path = self._get_output_path(image_path)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as PNG to preserve transparency
        img.save(output_path, format='PNG')
        
        return output_path
    
    def _backup_image(self, image_path: str) -> str:
        """
        Create a backup of the original image using shutil.copy for efficiency.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Path to the backup file
        """
        backup_dir = os.path.expanduser(self.config["general"]["backup_dir"])
        filename = os.path.basename(image_path)
        backup_filename = f"{os.path.splitext(filename)[0]}_backup{os.path.splitext(filename)[1]}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            # Use shutil.copy instead of PIL for efficiency
            shutil.copy2(image_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            return ""
    
    def _get_output_path(self, image_path: str) -> str:
        """
        Generate output path for processed image.
        
        Args:
            image_path: Path to the original image
            
        Returns:
            Path for the processed image
        """
        output_dir = os.path.expanduser(self.config["general"]["output_dir"])
        filename = os.path.basename(image_path)
        # Always use .png extension to ensure transparency support
        output_filename = f"{os.path.splitext(filename)[0]}_xshot.png"
        return os.path.join(output_dir, output_filename)
    
    def _add_titlebar(self, img: Image.Image) -> Image.Image:
        """
        Add a titlebar to the image.
        
        Args:
            img: PIL Image object
            
        Returns:
            Image with titlebar added
        """
        width, height = img.size
        titlebar_height = int(height * 0.05)  # 5% of image height
        titlebar_color = self._get_color_from_theme("header_bg")
        
        # Create a new image with space for the titlebar
        new_img = Image.new("RGBA", (width, height + titlebar_height), (0, 0, 0, 0))
        new_img.paste(img, (0, titlebar_height), mask=img if img.mode == 'RGBA' else None)
        
        # Draw the titlebar
        draw = ImageDraw.Draw(new_img)
        draw.rectangle(((0, 0), (width, titlebar_height)), fill=titlebar_color)
        
        # Add window control buttons (red, yellow, green)
        button_radius = int(titlebar_height * 0.3)
        button_padding = int(titlebar_height * 0.5)
        button_y = titlebar_height // 2
        
        # Red button (close)
        draw.ellipse(
            [(button_padding - button_radius, button_y - button_radius),
             (button_padding + button_radius, button_y + button_radius)],
            fill="#FF5F56"
        )
        
        # Yellow button (minimize)
        draw.ellipse(
            [(button_padding * 2 + button_radius - button_radius, button_y - button_radius),
             (button_padding * 2 + button_radius + button_radius, button_y + button_radius)],
            fill="#FFBD2E"
        )
        
        # Green button (maximize)
        draw.ellipse(
            [(button_padding * 3 + button_radius * 2 - button_radius, button_y - button_radius),
             (button_padding * 3 + button_radius * 2 + button_radius, button_y + button_radius)],
            fill="#27C93F"
        )
        
        # Add title text if enabled
        if self.config["titlebar"]["show_device_info"]:
            title_text = self._get_device_info()
        elif self.config["titlebar"]["custom_text"]:
            title_text = self.config["titlebar"]["custom_text"]
        else:
            # Safe filename extraction
            try:
                title_text = os.path.basename(getattr(img, 'filename', 'Screenshot'))
            except:
                title_text = "Screenshot"
        
        # Load font with enhanced cross-platform support
        font_size = self.config["titlebar"]["size"]
        font = self._load_font("mono", font_size)
        
        # Calculate text position (centered) with bounds checking
        try:
            text_width = draw.textlength(title_text, font=font)
        except AttributeError:
            # Fallback for older PIL versions
            text_width = draw.textsize(title_text, font=font)[0]
        
        text_x = (width - text_width) // 2
        text_y = (titlebar_height - font_size) // 2
        
        # Ensure text fits within titlebar bounds
        if text_x < button_padding * 4 + button_radius * 6:  # Account for control buttons
            text_x = button_padding * 4 + button_radius * 6
        if text_x + text_width > width - button_padding:
            text_x = width - text_width - button_padding
        
        # Draw text
        text_color = self._get_color_from_theme("header_fg")
        draw.text((text_x, text_y), title_text, fill=text_color, font=font)
        
        return new_img
    
    def _add_border_and_shadow(self, img: Image.Image) -> Image.Image:
        """
        Add border and shadow to the image.
        
        Args:
            img: PIL Image object
            
        Returns:
            Image with border and shadow added
        """
        width, height = img.size
        border_size = self.config["border"]["size"]
        border_radius = self.config["border"]["radius"]
        
        # Determine border color based on theme
        if self.theme_data["name"].lower() == "light":
            border_color = self.config["border"]["color_light"]
        else:
            border_color = self.config["border"]["color_dark"]
        
        # Create a new image with space for the border
        new_width = width + (border_size * 2)
        new_height = height + (border_size * 2)
        new_img = Image.new("RGBA", (new_width, new_height), border_color)
        
        # Paste the original image in the center
        new_img.paste(img, (border_size, border_size), mask=img if img.mode == 'RGBA' else None)
        
        # Add shadow if enabled
        shadow_size = self.config["border"]["shadow_size"].split('x')
        if len(shadow_size) >= 2:
            try:
                blur_radius = int(shadow_size[0])
                shadow_offset = int(shadow_size[1].split('+')[0])
                
                # Create shadow
                shadow = Image.new("RGBA", new_img.size, (0, 0, 0, 0))
                shadow_draw = ImageDraw.Draw(shadow)
                shadow_draw.rectangle(
                    ((border_size - shadow_offset, border_size - shadow_offset),
                     (new_width - border_size + shadow_offset, new_height - border_size + shadow_offset)),
                    fill=self.config["border"]["shadow_color"]
                )
                shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
                
                # Composite shadow and image
                result = Image.alpha_composite(shadow, new_img)
                return result
            except Exception as e:
                print(f"Error adding shadow: {e}")
        
        return new_img
    
    def _add_text_elements(self, img: Image.Image) -> Image.Image:
        """
        Add all text elements (headers, footers, custom) to the image using the advanced TextRenderer.
        
        Args:
            img: PIL Image object
            
        Returns:
            Image with all text elements added
        """
        # Use the advanced TextRenderer for comprehensive text rendering
        return self.text_renderer.render_all_text(img)
    
    def _add_footer(self, img: Image.Image) -> Image.Image:
        """
        Legacy footer method - now redirects to comprehensive text rendering.
        Maintained for backwards compatibility.
        
        Args:
            img: PIL Image object
            
        Returns:
            Image with text elements added
        """
        return self._add_text_elements(img)
    
    def _add_custom_image(self, img: Image.Image) -> Image.Image:
        """
        Add custom image to the screenshot.
        
        Args:
            img: PIL Image object
            
        Returns:
            Image with custom image added
        """
        if not self.config["custom_image"]["path"]:
            return img
            
        try:
            # Open custom image
            custom_img_path = os.path.expanduser(self.config["custom_image"]["path"])
            if not os.path.exists(custom_img_path):
                return img
                
            custom_img = Image.open(custom_img_path)
            
            # Convert to RGBA if not already
            if custom_img.mode != 'RGBA':
                custom_img = custom_img.convert('RGBA')
            
            # Resize custom image if needed
            target_size = self.config["custom_image"]["size"]
            if target_size > 0:
                # Calculate aspect ratio
                width, height = custom_img.size
                ratio = min(target_size / width, target_size / height)
                new_size = (int(width * ratio), int(height * ratio))
                custom_img = custom_img.resize(new_size, Image.LANCZOS)
            
            # Determine position
            position = self.config["custom_image"]["position"].lower()
            padding = self.config["custom_image"]["padding"]
            width, height = img.size
            custom_width, custom_height = custom_img.size
            
            if position == "top-left":
                pos_x = padding
                pos_y = padding
            elif position == "top-right":
                pos_x = width - custom_width - padding
                pos_y = padding
            elif position == "bottom-left":
                pos_x = padding
                pos_y = height - custom_height - padding
            elif position == "bottom-right":
                pos_x = width - custom_width - padding
                pos_y = height - custom_height - padding
            else:
                # Default to bottom-left
                pos_x = padding
                pos_y = height - custom_height - padding
            
            # Paste custom image with transparency
            img.paste(custom_img, (pos_x, pos_y), custom_img)
            
            return img
        except Exception as e:
            print(f"Error adding custom image: {e}")
            return img
    
    def _get_device_info(self) -> str:
        """
        Get device information for titlebar with improved Linux distro detection.
        
        Returns:
            Device information string
        """
        system = platform.system()
        if system == "Linux":
            # Try multiple methods to get Linux distribution info
            distro_name = "Linux"
            version = platform.release()
            
            try:
                # Method 1: Try to get Android device info if running on Termux
                if os.path.exists("/system/build.prop"):
                    # Running on Android/Termux
                    manufacturer = self._safe_subprocess_output(["getprop", "ro.product.manufacturer"]).strip().upper()
                    model = self._safe_subprocess_output(["getprop", "ro.product.model"]).strip()
                    android_ver = self._safe_subprocess_output(["getprop", "ro.build.version.release"]).strip()
                    
                    if manufacturer and model and android_ver:
                        return f"{manufacturer} {model} | Android {android_ver}"
                
                # Method 2: Try lsb_release command
                lsb_output = self._safe_subprocess_output(["lsb_release", "-ds"]).strip()
                if lsb_output:
                    return lsb_output.replace('"', '')
                
                # Method 3: Try /etc/os-release file
                if os.path.exists("/etc/os-release"):
                    with open("/etc/os-release", "r") as f:
                        os_release = {}
                        for line in f:
                            if "=" in line:
                                key, value = line.strip().split("=", 1)
                                os_release[key] = value.strip('"')
                        
                        if "PRETTY_NAME" in os_release:
                            return os_release["PRETTY_NAME"]
                        elif "NAME" in os_release and "VERSION" in os_release:
                            return f"{os_release['NAME']} {os_release['VERSION']}"
                        elif "NAME" in os_release:
                            return os_release["NAME"]
                
                # Method 4: Try /etc/issue file
                if os.path.exists("/etc/issue"):
                    with open("/etc/issue", "r") as f:
                        issue = f.read().strip()
                        if issue:
                            return issue.split("\\&quot;")[0].strip()
                
                # Method 5: Try /etc/*-release files
                for release_file in ["/etc/debian_version", "/etc/redhat-release", "/etc/fedora-release"]:
                    if os.path.exists(release_file):
                        with open(release_file, "r") as f:
                            content = f.read().strip()
                            if content:
                                return f"{os.path.basename(release_file).split('_')[0].capitalize()} {content}"
                
            except Exception as e:
                print(f"Error getting device info: {e}")
            
            # Fallback to basic Linux info
            return f"Linux {version}"
        elif system == "Darwin":
            return f"macOS {platform.mac_ver()[0]}"
        elif system == "Windows":
            return f"Windows {platform.release()}"
        else:
            return system
    
    def _safe_subprocess_output(self, command):
        """
        Safely execute a subprocess command and return its output.
        
        Args:
            command: Command to execute
            
        Returns:
            Command output or empty string on error
        """
        try:
            return subprocess.check_output(command, universal_newlines=True, stderr=subprocess.DEVNULL)
        except (subprocess.SubprocessError, FileNotFoundError):
            return ""
    
    def _get_color_from_theme(self, key: str) -> str:
        """
        Get color from theme data.
        
        Args:
            key: Color key
            
        Returns:
            Color value
        """
        if key in self.theme_data["ui"]:
            return self.theme_data["ui"][key]
        elif key in self.theme_data["colors"]:
            return self.theme_data["colors"][key]
        else:
            # Default fallback colors
            defaults = {
                "header_bg": "#1E222B",
                "header_fg": "#F8F9FA",
                "footer_bg": "#1E222B",
                "footer_fg": "#F8F9FA",
                "background": "#1E222B",
                "foreground": "#F8F9FA",
                "accent": "#59d6ff",
                "border": "#3d465c",
            }
            return defaults.get(key, "#000000")
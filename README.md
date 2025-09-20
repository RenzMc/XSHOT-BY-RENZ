# 📸 XShot - Advanced Screenshot Enhancement Tool

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/RenzMc/XSHOT)

XShot is a powerful, highly customizable screenshot enhancement tool built in Python that transforms your ordinary screenshots into professional, polished images. Perfect for developers, content creators, and anyone who wants to make their screenshots stand out.

## ✨ Features

### 🎨 **Visual Enhancements**
- **Custom Headers & Footers**: Add professional headers and footers with customizable text, styling, and positioning
- **Custom PNG Watermarks**: Add your own PNG images to any corner (top-left, top-right, bottom-left, bottom-right) with adjustable size and padding
- **Professional Borders**: Rounded borders with customizable colors, shadows, and opacity
- **Multiple Themes**: Dark, Light, Nord, Dracula, and custom theme support
- **Advanced Typography**: Multiple font families (mono, sans, serif, modern, classic, minimal) with style options

### 🛠 **Customization Options**

#### **Header Settings**
- ✅ Enable/disable headers
- ✅ Custom text and positioning
- ✅ Background colors and borders
- ✅ Time display with custom formats
- ✅ Font family and style options
- ✅ Text shadows and outlines
- ✅ Custom opacity and padding

#### **Footer Settings**
- ✅ Device information display
- ✅ Custom text elements
- ✅ Professional styling options
- ✅ Gradient backgrounds
- ✅ Flexible positioning

#### **Custom PNG Images** 🎯
- ✅ **Size editing**: Adjust image size in pixels through the UI
- ✅ **Position control**: Place in any corner (bottom-left/right supported)
- ✅ **Padding adjustment**: Fine-tune spacing around images
- ✅ **Enable/disable**: Toggle watermarks on/off
- ✅ **Path configuration**: Set custom image paths
- ✅ **Real-time preview**: See changes instantly

#### **Advanced Features**
- ✅ Auto-detection mode with file watching
- ✅ Batch processing capabilities
- ✅ Titlebar customization
- ✅ Theme switching
- ✅ Configuration management
- ✅ Cross-platform font handling

### 🖥 **Operating System Support**

| OS | Support | Tested Versions |
|---|---|---|
| **Linux** | ✅ Full Support | Ubuntu 20.04+, Debian 11+, Arch Linux, Fedora 35+ |
| **macOS** | ✅ Full Support | macOS 11.0+ (Big Sur and later) |
| **Windows** | ✅ Full Support | Windows 10/11 (with WSL recommended) |

### 📋 **System Requirements**

- **Python**: 3.11 or higher
- **Memory**: 256MB RAM minimum (512MB recommended)
- **Storage**: 100MB available space
- **Graphics**: Basic graphics support for image processing
- **Dependencies**: Pillow, Rich, Click, Watchdog, PyYAML, NumPy

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/RenzMc/XSHOT.git
cd XSHOT/xshot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run XShot**:
```bash
# Manual mode - Interactive UI
python -m xshot_py.main -m

# Auto mode - Watch directories
python -m xshot_py.main -a

# Show help
python -m xshot_py.main --help
```

### Alternative Installation

```bash
# Automatic installation (if install.sh exists)
bash install.sh

# Or manual package installation
pip install -e .
xshot  # Run from anywhere
```

## 📖 Usage Guide

### Manual Mode (Interactive)

Process individual screenshots with full control:

```bash
python -m xshot_py.main -m
```

**Workflow:**
1. Enter the path to your screenshot file
2. Access Settings menu (option 3) to customize:
   - **Option 6: Custom Image Settings** - Edit PNG watermarks
   - **Option 5: Header Settings** - Configure headers
   - **Option 4: Footer Settings** - Setup footers
   - **Option 1: Theme Settings** - Choose visual themes
3. Process and save enhanced screenshot

### Auto Mode (Background Processing)

Automatically process screenshots as they're created:

```bash
python -m xshot_py.main -a
```

**Features:**
- Watches specified directories for new files
- Processes files matching configured patterns
- Applies predefined enhancement settings
- Saves to configured output directory
- Runs continuously in background

### Command Line Options

```bash
usage: main.py [-h] [-a] [-m] [-t THEME] [-i INPUT] [-o OUTPUT]
               [--no-titlebar] [--no-footer] [--no-custom-image]
               [--config CONFIG] [--list-themes]

XShot - Screenshot Enhancement Tool

options:
  -h, --help            Show help message and exit
  -a, --auto            Run in auto screenshot mode
  -m, --manual          Run in manual screenshot mode
  -t THEME, --theme     Set theme (dark, light, nord, dracula)
  -i INPUT, --input     Input file to process
  -o OUTPUT, --output   Output directory
  --no-titlebar         Disable titlebar rendering
  --no-footer           Disable footer rendering
  --no-custom-image     Disable custom image watermarks
  --config CONFIG       Path to custom config directory
  --list-themes         List all available themes
```

## ⚙️ Configuration & Settings

### Interactive Settings Menu

Access comprehensive settings through the UI:

```
Settings Menu:
├── 1. Theme Settings      - Visual themes and colors
├── 2. Border Settings     - Borders, shadows, styles  
├── 3. Titlebar Settings   - Window titlebar appearance
├── 4. Footer Settings     - Footer content and styling
├── 5. Header Settings     - Header text and formatting
├── 6. Custom Image Settings - PNG watermark configuration
└── 7. Auto Detection Settings - File watching settings
```

### Custom PNG Watermark Configuration 🎯

**Access**: Settings Menu → Option 6: Custom Image Settings

**Editable Properties:**
```yaml
Custom Image Settings:
├── Enabled: [Yes/No] - Toggle watermark on/off
├── Image Path: [Text Input] - Path to your PNG file
├── Position: [Choice] 
│   ├── top-left      - Top left corner
│   ├── top-right     - Top right corner  
│   ├── bottom-left   - Bottom left corner ✅
│   └── bottom-right  - Bottom right corner ✅
├── Size: [Number Input] - Size in pixels (e.g., 100px) ✅ EDITABLE
└── Padding: [Number Input] - Spacing in pixels (e.g., 20px) ✅ EDITABLE
```

**Example Configuration Session:**
```
Custom Image Settings
Current Settings:
Enabled: Yes
Image Path: /path/to/logo.png
Position: bottom-right
Size: 150px          ← User can edit this
Padding: 25px        ← User can edit this

Edit Settings:
Enabled [Y/n]: y
Image Path: /home/user/watermark.png
Position [top-left/top-right/bottom-left/bottom-right]: bottom-right
Size (px) [150]: 200     ← User types new size
Padding (px) [25]: 30    ← User types new padding

✅ Settings saved!
```

### Theme Customization

**Built-in Themes:**
- **Dark**: Professional dark mode with blue accents
- **Light**: Clean light theme with minimal contrast
- **Nord**: Nordic-inspired color palette
- **Dracula**: Popular purple-based dark theme

**Custom Theme Creation:**
```yaml
# ~/.config/xshot/themes/my_theme.yaml
name: "My Custom Theme"
background: "#1a1a1a"
text_color: "#ffffff"
accent_color: "#00ff88"
border_color: "#333333"
# ... more customization options
```

### Configuration Files

**Main Config Location:**
```
~/.config/xshot/
├── config.yaml          - Main configuration
├── themes/              - Custom themes directory
│   ├── dark.yaml
│   ├── light.yaml
│   └── custom.yaml
└── cache/               - Temporary files
```

## 🎯 Usage Examples

### Basic Processing

```bash
# Process single file with dark theme
python -m xshot_py.main -i screenshot.png -t dark -o ./enhanced/

# Process without footer
python -m xshot_py.main -i screenshot.png --no-footer

# Process with custom config directory
python -m xshot_py.main -i screenshot.png --config ./my-config/
```

### Batch Processing with Auto Mode

1. **Setup Auto Detection:**
```bash
python -m xshot_py.main -a
# Go to Settings → Auto Detection Settings
# Add watch directories: ~/Screenshots, ~/Desktop
# Set file patterns: *.png, *.jpg, *.jpeg
# Configure output directory: ~/Enhanced_Screenshots
```

2. **Configure Custom Watermark:**
```bash
# Settings → Custom Image Settings
# Enable: Yes
# Image Path: ~/logo.png
# Position: bottom-right
# Size: 120px (editable)
# Padding: 15px (editable)
```

3. **Let XShot automatically enhance new screenshots!**

### Content Creator Workflow

```bash
# Perfect setup for streamers/YouTubers
python -m xshot_py.main -m

# Configure settings:
# - Header: Channel name + timestamp
# - Footer: Website URL + social media
# - Custom PNG: Channel logo (bottom-right, 100px)
# - Theme: Dark with brand colors
# - Border: Rounded with subtle shadow
```

## 🔧 Advanced Features

### Font Management

**Automatic Font Detection:**
- **Mono Fonts**: JetBrains Mono → DejaVu Sans Mono → Liberation Mono
- **Sans Fonts**: Inter → DejaVu Sans → Liberation Sans  
- **Serif Fonts**: Playfair Display → DejaVu Serif → Liberation Serif

**Cross-Platform Fallbacks:**
- Linux: System fonts + bundled fonts
- macOS: System fonts + custom fonts
- Windows: System fonts + packaged fonts

### Rendering Pipeline

**Advanced Image Processing:**
```
Input Screenshot
    ↓
Border & Shadow Addition
    ↓  
Header Rendering (if enabled)
    ↓
Footer Rendering (if enabled)  
    ↓
Custom PNG Overlay (if enabled)
    ↓
Theme Application
    ↓
Final Enhanced Screenshot
```

**Rendering Features:**
- Anti-aliasing for smooth edges
- Alpha blending for transparency
- Gradient backgrounds support
- Multiple shadow types
- Border radius with proper clipping

### File Watching System

**Auto-Detection Capabilities:**
- Real-time directory monitoring
- Configurable file patterns
- Instant processing of new files
- Duplicate detection and handling
- Error recovery and logging

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YourUsername/XSHOT.git
cd XSHOT

# 2. Create development environment  
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -r requirements.txt
pip install -e .

# 4. Run tests
python -m pytest tests/

# 5. Create feature branch
git checkout -b feature/awesome-feature

# 6. Make changes and test
python -m xshot_py.main -m  # Test your changes

# 7. Submit pull request
```

### Contribution Guidelines

- **Code Style**: Follow PEP 8 with 100-character line limit
- **Testing**: Add tests for new features
- **Documentation**: Update README and docstrings
- **Commits**: Use conventional commit messages
- **Issues**: Use issue templates for bug reports

## 🐛 Troubleshooting

### Common Issues

**1. Font Loading Errors**
```bash
# Install system fonts
sudo apt install fonts-dejavu fonts-liberation  # Ubuntu/Debian
brew install font-dejavu font-liberation        # macOS
```

**2. Permission Errors (Auto Mode)**
```bash
# Ensure read permissions on watch directories
chmod +r ~/Screenshots
```

**3. Custom PNG Not Appearing**
```bash
# Check file path and format
file ~/logo.png  # Should show PNG image data
# Ensure PNG has transparency/alpha channel for proper blending
```

**4. Performance Issues**
```bash
# Reduce image size for faster processing
# Use smaller custom PNG sizes
# Enable fewer visual effects
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Bug Reports**: [GitHub Issues](https://github.com/RenzMc/XSHOT/issues)
- **Community**: [Discord Server](https://discord.gg/xshot) (Coming Soon)

## 🙏 Acknowledgments

- **[Pillow](https://python-pillow.org/)** - Powerful Python Imaging Library
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal formatting and UI
- **[Click](https://click.palletsprojects.com/)** - Elegant command line interfaces
- **[Watchdog](https://pythonhosting.org/watchdog/)** - File system monitoring
- **[PyYAML](https://pyyaml.org/)** - YAML parser and emitter
- **[NumPy](https://numpy.org/)** - Numerical computing support

---

<div align="center">

**Made with ❤️ by [RenzMc](https://github.com/RenzMc)**

*Transform your screenshots into professional masterpieces with XShot!*

[![GitHub Stars](https://img.shields.io/github/stars/RenzMc/XSHOT?style=social)](https://github.com/RenzMc/XSHOT/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/RenzMc/XSHOT?style=social)](https://github.com/RenzMc/XSHOT/network/members)

</div>
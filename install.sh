#!/bin/bash
# XShot Installation Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}XShot Installation Script${NC}"
echo -e "${YELLOW}=============================${NC}"

# Detect OS and package manager
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    
    # Check for Termux
    if [ -d "/data/data/com.termux" ]; then
        IS_TERMUX=true
        PREFIX="/data/data/com.termux/files/usr"
        HOME="/data/data/com.termux/files/home"
        PACKAGE_MANAGER="pkg"
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        IS_TERMUX=false
        PREFIX="/usr"
        
        # Determine package manager
        if command -v apt-get &> /dev/null; then
            PACKAGE_MANAGER="apt-get"
            INSTALL_CMD="apt-get install -y"
        elif command -v dnf &> /dev/null; then
            PACKAGE_MANAGER="dnf"
            INSTALL_CMD="dnf install -y"
        elif command -v yum &> /dev/null; then
            PACKAGE_MANAGER="yum"
            INSTALL_CMD="yum install -y"
        elif command -v pacman &> /dev/null; then
            PACKAGE_MANAGER="pacman"
            INSTALL_CMD="pacman -S --noconfirm"
        elif command -v zypper &> /dev/null; then
            PACKAGE_MANAGER="zypper"
            INSTALL_CMD="zypper install -y"
        elif command -v apk &> /dev/null; then
            PACKAGE_MANAGER="apk"
            INSTALL_CMD="apk add"
        else
            echo -e "${RED}Unsupported package manager. Please install Python 3, pip, and ImageMagick manually.${NC}"
            PACKAGE_MANAGER="unknown"
        fi
        
        # Determine Python command
        if command -v python3 &> /dev/null; then
            PYTHON_CMD="python3"
        elif command -v python &> /dev/null; then
            PYTHON_CMD="python"
        else
            echo -e "${RED}Python not found. Please install Python 3.${NC}"
            exit 1
        fi
        
        # Determine pip command
        if command -v pip3 &> /dev/null; then
            PIP_CMD="pip3"
        elif command -v pip &> /dev/null; then
            PIP_CMD="pip"
        else
            echo -e "${RED}pip not found. Please install pip.${NC}"
            exit 1
        fi
    fi
else
    echo -e "${RED}Cannot determine OS. Please install Python 3, pip, and ImageMagick manually.${NC}"
    exit 1
fi

echo -e "${YELLOW}Detected OS: $OS${NC}"
echo -e "${YELLOW}Package Manager: $PACKAGE_MANAGER${NC}"
echo -e "${YELLOW}Python Command: $PYTHON_CMD${NC}"
echo -e "${YELLOW}Pip Command: $PIP_CMD${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
if [ "$IS_TERMUX" = true ]; then
    pkg update -y
    pkg install -y python imagemagick python-pip termux-api wget
    
    # Setup storage access
    termux-setup-storage
else
    if [ "$PACKAGE_MANAGER" != "unknown" ]; then
        # Update package lists
        if [ "$PACKAGE_MANAGER" = "apt-get" ]; then
            sudo apt-get update
        elif [ "$PACKAGE_MANAGER" = "dnf" ] || [ "$PACKAGE_MANAGER" = "yum" ]; then
            sudo $PACKAGE_MANAGER check-update
        elif [ "$PACKAGE_MANAGER" = "pacman" ]; then
            sudo pacman -Sy
        elif [ "$PACKAGE_MANAGER" = "zypper" ]; then
            sudo zypper refresh
        elif [ "$PACKAGE_MANAGER" = "apk" ]; then
            sudo apk update
        fi
        
        # Install packages
        if [ "$PACKAGE_MANAGER" = "apt-get" ]; then
            sudo apt-get install -y python3 python3-pip imagemagick
        elif [ "$PACKAGE_MANAGER" = "dnf" ] || [ "$PACKAGE_MANAGER" = "yum" ]; then
            sudo $PACKAGE_MANAGER install -y python3 python3-pip ImageMagick
        elif [ "$PACKAGE_MANAGER" = "pacman" ]; then
            sudo pacman -S --noconfirm python python-pip imagemagick
        elif [ "$PACKAGE_MANAGER" = "zypper" ]; then
            sudo zypper install -y python3 python3-pip ImageMagick
        elif [ "$PACKAGE_MANAGER" = "apk" ]; then
            sudo apk add python3 py3-pip imagemagick
        fi
    else
        echo -e "${YELLOW}Please ensure Python 3, pip, and ImageMagick are installed.${NC}"
    fi
fi

# Create installation directory
INSTALL_DIR="$HOME/.xshot"
echo -e "${YELLOW}Creating installation directory: $INSTALL_DIR${NC}"
mkdir -p "$INSTALL_DIR"

# Copy files
echo -e "${YELLOW}Copying files...${NC}"
cp -r "$(dirname "$0")"/* "$INSTALL_DIR/"

# Create config directory
CONFIG_DIR="$HOME/.config/xshot"
echo -e "${YELLOW}Creating config directory: $CONFIG_DIR${NC}"
mkdir -p "$CONFIG_DIR/themes"

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
$PIP_CMD install -r "$INSTALL_DIR/requirements.txt"

# Install XShot as a Python package
echo -e "${YELLOW}Installing XShot as a Python package...${NC}"
cd "$INSTALL_DIR"
$PIP_CMD install -e .

# Create executable script
if [ "$IS_TERMUX" = true ]; then
    # Create bin directory if it doesn't exist
    mkdir -p "$PREFIX/bin"
    
    # Create executable script
    cat > "$PREFIX/bin/xshot" << EOF
#!/bin/bash
$PYTHON_CMD -m xshot_py.main "\$@"
EOF
    
    # Make executable
    chmod +x "$PREFIX/bin/xshot"
else
    # Create user bin directory if it doesn't exist
    mkdir -p "$HOME/.local/bin"
    
    # Create executable script
    cat > "$HOME/.local/bin/xshot" << EOF
#!/bin/bash
$PYTHON_CMD -m xshot_py.main "\$@"
EOF
    
    # Make executable
    chmod +x "$HOME/.local/bin/xshot"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "${YELLOW}Adding $HOME/.local/bin to PATH in .bashrc${NC}"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo -e "${YELLOW}Please restart your terminal or run 'source ~/.bashrc' to update your PATH.${NC}"
    fi
fi

# Setup assets
echo -e "${YELLOW}Setting up assets...${NC}"
mkdir -p "$INSTALL_DIR/xshot_py/assets/fonts"

# Download JetBrains Mono font if not available
echo -e "${YELLOW}Downloading default fonts...${NC}"
if [ "$IS_TERMUX" = true ]; then
    pkg install -y wget
fi

FONT_URL="https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/JetBrainsMono/Medium/complete/JetBrains%20Mono%20Medium%20Nerd%20Font%20Complete.ttf"
wget -q "$FONT_URL" -O "$INSTALL_DIR/xshot_py/assets/fonts/JetBrains Mono Medium Nerd Font Complete.ttf"

echo -e "${GREEN}XShot has been installed successfully!${NC}"
echo -e "${YELLOW}Run 'xshot' to start the application.${NC}"
echo -e "${YELLOW}If the command is not found, you may need to add ~/.local/bin to your PATH or restart your terminal.${NC}"
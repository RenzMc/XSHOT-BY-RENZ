#!/bin/bash
# XShot Uninstallation Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}XShot Uninstallation Script${NC}"
echo -e "${YELLOW}=============================${NC}"

# Check if running on Termux
if [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
    PREFIX="/data/data/com.termux/files/usr"
    HOME="/data/data/com.termux/files/home"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    IS_TERMUX=false
    PREFIX="/usr"
    
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

# Ask for confirmation
echo -e "${YELLOW}This will uninstall XShot from your system.${NC}"
echo -e "${YELLOW}Do you want to continue? (y/n)${NC}"
read -r CONFIRM

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo -e "${YELLOW}Uninstallation cancelled.${NC}"
    exit 0
fi

# Uninstall Python package
echo -e "${YELLOW}Uninstalling XShot Python package...${NC}"
$PIP_CMD uninstall -y xshot

# Remove executable
if [ "$IS_TERMUX" = true ]; then
    echo -e "${YELLOW}Removing executable...${NC}"
    rm -f "$PREFIX/bin/xshot"
else
    echo -e "${YELLOW}Removing executable...${NC}"
    rm -f "$HOME/.local/bin/xshot"
fi

# Ask if user wants to remove configuration files
echo -e "${YELLOW}Do you want to remove configuration files? (y/n)${NC}"
read -r REMOVE_CONFIG

if [[ "$REMOVE_CONFIG" == "y" || "$REMOVE_CONFIG" == "Y" ]]; then
    echo -e "${YELLOW}Removing configuration files...${NC}"
    rm -rf "$HOME/.config/xshot"
    echo -e "${GREEN}Configuration files removed.${NC}"
else
    echo -e "${YELLOW}Configuration files kept.${NC}"
fi

# Ask if user wants to remove installation directory
echo -e "${YELLOW}Do you want to remove the installation directory? (y/n)${NC}"
read -r REMOVE_INSTALL

if [[ "$REMOVE_INSTALL" == "y" || "$REMOVE_INSTALL" == "Y" ]]; then
    echo -e "${YELLOW}Removing installation directory...${NC}"
    rm -rf "$HOME/.xshot"
    echo -e "${GREEN}Installation directory removed.${NC}"
else
    echo -e "${YELLOW}Installation directory kept.${NC}"
fi

echo -e "${GREEN}XShot has been uninstalled successfully!${NC}"
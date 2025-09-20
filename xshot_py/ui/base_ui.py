"""
Base UI for XShot

This module provides the base UI components for the XShot application.
"""

from typing import Dict, Any, List, Optional, Callable
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.live import Live
from rich.box import Box, ROUNDED

from xshot_py.config.config_manager import ConfigManager
from xshot_py.themes.theme_manager import ThemeManager

class BaseUI:
    """
    Base UI class for XShot.
    """
    
    def __init__(self, config_manager: ConfigManager, theme_manager: ThemeManager):
        """
        Initialize the base UI.
        
        Args:
            config_manager: Configuration manager instance
            theme_manager: Theme manager instance
        """
        self.config_manager = config_manager
        self.theme_manager = theme_manager
        self.console = Console()
        
        # Get theme
        theme_id = self.config_manager.config["appearance"]["theme"]
        self.theme = self.theme_manager.get_theme(theme_id)
    
    def print_header(self, title: str) -> None:
        """
        Print a header.
        
        Args:
            title: Header title
        """
        self.console.print(f"[bold blue]{'=' * (len(title) + 4)}[/bold blue]")
        self.console.print(f"[bold blue]= [/bold blue][bold white]{title}[/bold white][bold blue] =[/bold blue]")
        self.console.print(f"[bold blue]{'=' * (len(title) + 4)}[/bold blue]")
        self.console.print()
    
    def create_header(self, title: str = "XShot", subtitle: str = "Screenshot Enhancement Tool") -> Panel:
        """
        Create a header panel.
        
        Args:
            title: Header title
            subtitle: Header subtitle
            
        Returns:
            Rich Panel object
        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row(f"[bold]{title}[/bold]")
        grid.add_row(f"[italic]{subtitle}[/italic]")
        
        return Panel(grid, box=ROUNDED)
    
    def create_footer(self, text: str = "Press Ctrl+C to exit") -> Panel:
        """
        Create a footer panel.
        
        Args:
            text: Footer text
            
        Returns:
            Rich Panel object
        """
        return Panel(Text(text, justify="center"), box=ROUNDED)
    
    def create_menu(self, title: str, options: List[Dict[str, Any]]) -> Panel:
        """
        Create a menu panel.
        
        Args:
            title: Menu title
            options: List of menu options
            
        Returns:
            Rich Panel object
        """
        table = Table(box=None, expand=True, show_header=False)
        table.add_column("Key", style="bold cyan", width=4)
        table.add_column("Option")
        table.add_column("Description", style="italic")
        
        for option in options:
            table.add_row(
                option.get("key", ""),
                option.get("name", ""),
                option.get("description", "")
            )
        
        return Panel(table, title=title, box=ROUNDED)
    
    def create_info_panel(self, title: str, content: Any) -> Panel:
        """
        Create an information panel.
        
        Args:
            title: Panel title
            content: Panel content
            
        Returns:
            Rich Panel object
        """
        return Panel(content, title=title, box=ROUNDED)
    
    def create_layout(self) -> Layout:
        """
        Create a layout for the UI.
        
        Returns:
            Rich Layout object
        """
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=1)
        )
        
        layout["main"].split_row(
            Layout(name="sidebar", ratio=1),
            Layout(name="content", ratio=3)
        )
        
        return layout
    
    def prompt(self, message: str, default: str = "", password: bool = False) -> str:
        """
        Prompt the user for input.
        
        Args:
            message: Prompt message
            default: Default value
            password: Whether to hide input
            
        Returns:
            User input
        """
        return Prompt.ask(message, default=default, password=password)
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """
        Prompt the user for confirmation.
        
        Args:
            message: Confirmation message
            default: Default value
            
        Returns:
            User confirmation
        """
        return Confirm.ask(message, default=default)
    
    def show_progress(self, message: str, callback: Callable, total: int = 100) -> None:
        """
        Show a progress bar.
        
        Args:
            message: Progress message
            callback: Function to call with progress object
            total: Total steps
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(message, total=total)
            callback(progress, task)
    
    def clear(self) -> None:
        """
        Clear the console.
        """
        self.console.clear()
    
    def print(self, *args, **kwargs) -> None:
        """
        Print to the console.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        self.console.print(*args, **kwargs)
    
    def rule(self, title: str = "", **kwargs) -> None:
        """
        Print a rule.
        
        Args:
            title: Rule title
            **kwargs: Keyword arguments
        """
        self.console.rule(title, **kwargs)
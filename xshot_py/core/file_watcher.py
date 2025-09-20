"""
File Watcher for XShot

This module handles watching directories for new files.
"""

import os
import time
from typing import Dict, Any, List, Callable, Optional
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

class ScreenshotHandler(FileSystemEventHandler):
    """
    Event handler for new screenshot files.
    """
    
    def __init__(self, patterns: List[str], callback: Callable[[str], None]):
        """
        Initialize the screenshot handler.
        
        Args:
            patterns: List of file patterns to watch for
            callback: Function to call when a new file is detected
        """
        self.patterns = patterns
        self.callback = callback
        self.last_processed = set()
    
    def on_created(self, event):
        """
        Handle file creation events.
        
        Args:
            event: File system event
        """
        if not event.is_directory:
            file_path = event.src_path
            
            # Check if the file matches any of the patterns
            if any(Path(file_path).match(pattern) for pattern in self.patterns):
                # Avoid processing the same file multiple times
                if file_path not in self.last_processed:
                    # Wait a moment to ensure the file is fully written
                    time.sleep(1)
                    
                    # Call the callback with the file path
                    self.callback(file_path)
                    
                    # Add to processed files
                    self.last_processed.add(file_path)
                    
                    # Limit the size of the set to avoid memory issues
                    if len(self.last_processed) > 100:
                        self.last_processed.pop()

class FileWatcher:
    """
    Watches directories for new files.
    """
    
    def __init__(self, config: Dict[str, Any], callback: Callable[[str], None]):
        """
        Initialize the file watcher.
        
        Args:
            config: Application configuration
            callback: Function to call when a new file is detected
        """
        self.config = config
        self.callback = callback
        self.observer = None
        self.handlers = []
    
    def start(self) -> bool:
        """
        Start watching for new files.
        
        Returns:
            True if started successfully, False otherwise
        """
        if not self.config["auto_detection"]["enabled"]:
            return False
            
        watch_dirs = self.config["auto_detection"]["watch_dirs"]
        patterns = self.config["auto_detection"]["file_patterns"]
        
        if not watch_dirs or not patterns:
            return False
            
        try:
            self.observer = Observer()
            
            # Add handlers for each directory
            for dir_path in watch_dirs:
                dir_path = os.path.expanduser(dir_path)
                
                if os.path.exists(dir_path) and os.path.isdir(dir_path):
                    handler = ScreenshotHandler(patterns, self.callback)
                    self.observer.schedule(handler, dir_path, recursive=False)
                    self.handlers.append(handler)
            
            # Start the observer
            self.observer.start()
            return True
        except Exception as e:
            print(f"Error starting file watcher: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop watching for new files.
        
        Returns:
            True if stopped successfully, False otherwise
        """
        if self.observer:
            try:
                self.observer.stop()
                self.observer.join()
                self.observer = None
                self.handlers = []
                return True
            except Exception as e:
                print(f"Error stopping file watcher: {e}")
                return False
        return False
    
    def is_running(self) -> bool:
        """
        Check if the file watcher is running.
        
        Returns:
            True if running, False otherwise
        """
        return self.observer is not None and self.observer.is_alive()
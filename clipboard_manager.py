"""
Clipboard Manager Module
Handles clipboard operations for copying commands.
"""

import pyperclip

class ClipboardManager:
    """Manages clipboard operations."""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Copy text to system clipboard.
        
        Args:
            text: Text to copy to clipboard
            
        Returns:
            bool: True if copied successfully, False otherwise
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
    
    @staticmethod
    def get_clipboard_text() -> str:
        """
        Get text from system clipboard.
        
        Returns:
            String from clipboard or empty string if error
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Error reading from clipboard: {e}")
            return ""
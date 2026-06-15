"""
Theme Manager Module
Handles application theming (light/dark mode) with gray color schemes.
"""

import json
import os
import PySimpleGUI as sg

class ThemeManager:
    """Manages application themes and user preferences."""
    
    def __init__(self, settings_file: str = "config/settings.json"):
        """
        Initialize the ThemeManager.
        
        Args:
            settings_file: Path to settings JSON file
        """
        self.settings_file = settings_file
        self.current_theme = self.load_theme_preference()
        
        # Define theme colors - Dark Gray and Light Gray
        self.themes = {
            "Dark Gray": {
                "background": "#2D2D2D",           # Dark gray background
                "text": "#E0E0E0",                 # Light gray text
                "button": ("#E0E0E0", "#3C3C3C"),  # Light text on darker button
                "button_hover": ("#FFFFFF", "#4A4A4A"),
                "input": "#3C3C3C",               # Slightly lighter than background
                "input_text": "#E0E0E0",
                "accent": "#6CB4EE",              # Soft blue accent
                "accent2": "#8BC34A",             # Soft green for success
                "error": "#EF5350",               # Soft red for errors
                "separator": "#4A4A4A",
                "border": "#3C3C3C",
                "scrollbar": "#4A4A4A",
                "selection": "#4A6FA5",
                "list_text": "#E0E0E0",
                "header_bg": "transparent",
                "title_color": "#6CB4EE",
                "subtitle_color": "#B0B0B0",
                "code_bg": "#363636",
                "code_text": "#A8D8A8",
                "favorite_color": "#FFD700"
            },
            "Light Gray": {
                "background": "#F0F0F0",           # Light gray background
                "text": "#333333",                 # Dark gray text
                "button": ("#333333", "#E0E0E0"),  # Dark text on light button
                "button_hover": ("#000000", "#D0D0D0"),
                "input": "#FFFFFF",               # White input
                "input_text": "#333333",
                "accent": "#2196F3",              # Blue accent
                "accent2": "#4CAF50",             # Green for success
                "error": "#F44336",               # Red for errors
                "separator": "#D0D0D0",
                "border": "#D0D0D0",
                "scrollbar": "#C0C0C0",
                "selection": "#BBDEFB",
                "list_text": "#333333",
                "header_bg": "transparent",
                "title_color": "#1976D2",
                "subtitle_color": "#666666",
                "code_bg": "#F5F5F5",
                "code_text": "#2E7D32",
                "favorite_color": "#F57F17"
            }
        }
        
    def load_theme_preference(self) -> str:
        """
        Load user's theme preference from settings file.
        
        Returns:
            Theme name string
        """
        if not os.path.exists(self.settings_file):
            return "Dark Gray"
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                return settings.get("theme", "Dark Gray")
        except (json.JSONDecodeError, FileNotFoundError):
            return "Dark Gray"
    
    def save_theme_preference(self) -> bool:
        """
        Save user's theme preference to settings file.
        
        Returns:
            bool: True if saved successfully
        """
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            settings = {}
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as file:
                    settings = json.load(file)
            
            settings["theme"] = self.current_theme
            
            with open(self.settings_file, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving theme preference: {e}")
            return False
    
    def set_theme(self, theme_name: str) -> None:
        """
        Set the current theme.
        
        Args:
            theme_name: Name of the theme to apply
        """
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_theme_preference()
            self.apply_theme()
    
    def apply_theme(self) -> None:
        """Apply the current theme to PySimpleGUI."""
        theme_colors = self.themes.get(self.current_theme, self.themes["Dark Gray"])
        
        # Set PySimpleGUI global options for transparent backgrounds
        sg.set_options(
            background_color=theme_colors["background"],
            text_color=theme_colors["text"],
            button_color=theme_colors["button"],
            input_elements_background_color=theme_colors["input"],
            input_text_color=theme_colors["input_text"],
            scrollbar_color=theme_colors["scrollbar"],
            text_element_background_color=None  # Make text backgrounds transparent
        )
        
    def get_theme_colors(self) -> dict:
        """
        Get the current theme colors.
        
        Returns:
            Dictionary of theme colors
        """
        return self.themes.get(self.current_theme, self.themes["Dark Gray"])
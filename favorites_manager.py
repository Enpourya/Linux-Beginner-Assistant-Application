"""
Favorites Manager Module
Handles saving and loading of user's favorite commands.
"""

import json
import os
from typing import List, Dict, Any

class FavoritesManager:
    """Manages the favorites system with persistence."""
    
    def __init__(self, favorites_file: str = "config/favorites.json"):
        """
        Initialize the FavoritesManager.
        
        Args:
            favorites_file: Path to the favorites JSON file
        """
        self.favorites_file = favorites_file
        self.favorites = self.load_favorites()
        
    def load_favorites(self) -> List[Dict[str, Any]]:
        """
        Load favorites from JSON file.
        
        Returns:
            List of favorite task dictionaries
        """
        if not os.path.exists(self.favorites_file):
            return []
        
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_favorites(self) -> bool:
        """
        Save favorites to JSON file.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.favorites_file), exist_ok=True)
            
            with open(self.favorites_file, 'w', encoding='utf-8') as file:
                json.dump(self.favorites, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving favorites: {e}")
            return False
    
    def add_favorite(self, task: Dict[str, Any]) -> bool:
        """
        Add a task to favorites.
        
        Args:
            task: Task dictionary to add
            
        Returns:
            bool: True if added successfully, False if already exists
        """
        # Check if task already in favorites
        for fav in self.favorites:
            if (fav.get("command") == task.get("command") and 
                fav.get("title") == task.get("title")):
                return False
        
        self.favorites.append(task)
        return self.save_favorites()
    
    def remove_favorite(self, task: Dict[str, Any]) -> bool:
        """
        Remove a task from favorites.
        
        Args:
            task: Task dictionary to remove
            
        Returns:
            bool: True if removed successfully, False if not found
        """
        for i, fav in enumerate(self.favorites):
            if (fav.get("command") == task.get("command") and 
                fav.get("title") == task.get("title")):
                self.favorites.pop(i)
                return self.save_favorites()
        return False
    
    def is_favorite(self, task: Dict[str, Any]) -> bool:
        """
        Check if a task is in favorites.
        
        Args:
            task: Task dictionary to check
            
        Returns:
            bool: True if task is a favorite
        """
        for fav in self.favorites:
            if (fav.get("command") == task.get("command") and 
                fav.get("title") == task.get("title")):
                return True
        return False
    
    def get_all_favorites(self) -> List[Dict[str, Any]]:
        """
        Get all favorite tasks.
        
        Returns:
            List of favorite task dictionaries
        """
        return self.favorites.copy()
"""
Data Manager Module
Handles loading and parsing of Linux command data from JSON files.
"""

import json
import os
from typing import Dict, List, Optional, Any

class DataManager:
    """Manages loading and querying of Linux command data."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the DataManager.
        
        Args:
            data_dir: Directory containing JSON data files
        """
        self.data_dir = data_dir
        self.current_data = None
        self.current_distribution = None
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
    def load_distribution_data(self, distribution: str) -> bool:
        """
        Load command data for a specific Linux distribution.
        
        Args:
            distribution: Name of the Linux distribution
            
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        # Convert distribution name to filename format
        filename = distribution.lower().replace(" ", "_") + ".json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Data file not found: {filepath}")
                
            with open(filepath, 'r', encoding='utf-8') as file:
                self.current_data = json.load(file)
                self.current_distribution = distribution
                return True
                
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.current_data = None
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            self.current_data = None
            return False
        except Exception as e:
            print(f"Unexpected error loading data: {e}")
            self.current_data = None
            return False
    
    def get_categories(self) -> List[str]:
        """
        Get all available categories for the current distribution.
        
        Returns:
            List of category names
        """
        if not self.current_data:
            return []
        
        categories = []
        for category in self.current_data.get("categories", []):
            categories.append(category["name"])
        return categories
    
    def get_tasks_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        """
        Get all tasks for a specific category.
        
        Args:
            category_name: Name of the category
            
        Returns:
            List of task dictionaries
        """
        if not self.current_data:
            return []
        
        for category in self.current_data.get("categories", []):
            if category["name"] == category_name:
                return category.get("tasks", [])
        return []
    
    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """
        Search tasks by title, description, or command.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching task dictionaries with category info
        """
        if not self.current_data or not query:
            return []
        
        query = query.lower()
        results = []
        
        for category in self.current_data.get("categories", []):
            for task in category.get("tasks", []):
                if (query in task.get("title", "").lower() or
                    query in task.get("description", "").lower() or
                    query in task.get("command", "").lower()):
                    # Add category info to task for reference
                    task_with_category = task.copy()
                    task_with_category["category"] = category["name"]
                    results.append(task_with_category)
        
        return results
    
    def get_available_distributions(self) -> List[str]:
        """
        Get list of available distributions from data files.
        
        Returns:
            List of distribution names
        """
        distributions = []
        
        if not os.path.exists(self.data_dir):
            return distributions
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                # Convert filename back to display name
                name = filename.replace(".json", "").replace("_", " ").title()
                # Handle special cases
                name = name.replace("Opensuse", "openSUSE")
                name = name.replace("Rocky Linux", "Rocky Linux")
                name = name.replace("Almalinux", "AlmaLinux")
                distributions.append(name)
        
        return sorted(distributions)
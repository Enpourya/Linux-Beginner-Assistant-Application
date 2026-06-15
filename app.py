"""
Main Application Module
Contains the primary application logic and GUI implementation.
"""

import PySimpleGUI as sg
from typing import Optional, Dict, Any
from data_manager import DataManager
from favorites_manager import FavoritesManager
from theme_manager import ThemeManager
from clipboard_manager import ClipboardManager

class LinuxAssistantApp:
    """Main application class for Linux Beginner Assistant."""
    
    def __init__(self):
        """Initialize the application components."""
        self.data_manager = DataManager()
        self.favorites_manager = FavoritesManager()
        self.theme_manager = ThemeManager()
        self.clipboard_manager = ClipboardManager()
        
        # Apply saved theme
        self.theme_manager.apply_theme()
        
        # Current state
        self.current_task = None
        self.showing_favorites = False
        self.current_category = None
        
    def create_welcome_window(self) -> sg.Window:
        """
        Create the welcome/distribution selection window.
        
        Returns:
            PySimpleGUI Window object
        """
        colors = self.theme_manager.get_theme_colors()
        
        # Get available distributions
        distributions = self.data_manager.get_available_distributions()
        
        if not distributions:
            distributions = ["No distributions found"]
        
        layout = [
            [sg.Text("Welcome to Linux Beginner Assistant!", 
                    font=("Segoe UI", 26, "bold"), 
                    text_color=colors["title_color"],
                    background_color=colors["background"])],
            [sg.Text("Select your Linux distribution to get started:", 
                    font=("Segoe UI", 13),
                    text_color=colors["subtitle_color"],
                    background_color=colors["background"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Listbox(values=distributions, 
                       size=(40, 12), 
                       key="-DIST-",
                       enable_events=True,
                       select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                       font=("Segoe UI", 11),
                       background_color=colors["input"],
                       text_color=colors["list_text"],
                       sbar_background_color=colors["scrollbar"],
                       sbar_trough_color=colors["background"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Button("Continue", key="-CONTINUE-", size=(15, 1), 
                      font=("Segoe UI", 11, "bold"),
                      button_color=colors["button"],
                      bind_return_key=True),
             sg.Button("Exit", size=(15, 1),
                      font=("Segoe UI", 11),
                      button_color=colors["button"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Text("Theme:", size=(6, 1),
                    font=("Segoe UI", 10),
                    text_color=colors["text"],
                    background_color=colors["background"]),
             sg.Combo(["Dark Gray", "Light Gray"], 
                     default_value=self.theme_manager.current_theme,
                     key="-THEME-",
                     enable_events=True,
                     size=(12, 1),
                     readonly=True,
                     font=("Segoe UI", 10),
                     background_color=colors["input"],
                     text_color=colors["input_text"],
                     button_background_color=colors["button"][1],
                     button_arrow_color=colors["button"][0])]
        ]
        
        return sg.Window("Linux Beginner Assistant - Welcome", 
                        layout, 
                        finalize=True,
                        element_justification='center',
                        background_color=colors["background"])
    
    def create_main_window(self) -> sg.Window:
        """
        Create the main application window.
        
        Returns:
            PySimpleGUI Window object
        """
        colors = self.theme_manager.get_theme_colors()
        
        # Get categories and tasks for the selected category
        categories = self.data_manager.get_categories()
        self.current_category = categories[0] if categories else None
        tasks = self.data_manager.get_tasks_by_category(self.current_category) if self.current_category else []
        task_titles = [task["title"] for task in tasks]
        
        # Left panel - Categories, search, and tasks
        left_panel = [
            [sg.Text("🔍 Search:", font=("Segoe UI", 11, "bold"),
                    text_color=colors["text"],
                    background_color=colors["background"])],
            [sg.Input(key="-SEARCH-", size=(30, 1), 
                     enable_events=True,
                     font=("Segoe UI", 10),
                     background_color=colors["input"],
                     text_color=colors["input_text"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Text("📁 Categories:", font=("Segoe UI", 13, "bold"),
                    text_color=colors["accent"],
                    background_color=colors["background"])],
            [sg.Listbox(values=categories,
                       size=(30, 8),
                       key="-CATEGORIES-",
                       enable_events=True,
                       select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                       font=("Segoe UI", 10),
                       background_color=colors["input"],
                       text_color=colors["list_text"],
                       sbar_background_color=colors["scrollbar"],
                       sbar_trough_color=colors["background"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Text("📝 Tasks:", font=("Segoe UI", 13, "bold"),
                    text_color=colors["accent"],
                    background_color=colors["background"])],
            [sg.Listbox(values=task_titles,
                       size=(30, 10),
                       key="-TASKS-",
                       enable_events=True,
                       select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                       font=("Segoe UI", 10),
                       background_color=colors["input"],
                       text_color=colors["list_text"],
                       sbar_background_color=colors["scrollbar"],
                       sbar_trough_color=colors["background"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Button("⭐ Favorites", key="-FAVORITES-", size=(15, 1),
                      font=("Segoe UI", 10, "bold"),
                      button_color=(colors["favorite_color"], colors["button"][1])),
             sg.Button("📋 Show All", key="-ALL_TASKS-", size=(12, 1),
                      font=("Segoe UI", 10),
                      button_color=colors["button"])]
        ]
        
        # Right panel - Task details
        right_panel = [
            [sg.Text("", key="-TASK_TITLE-", font=("Segoe UI", 20, "bold"),
                    text_color=colors["title_color"],
                    background_color=colors["background"],
                    size=(50, 1))],
            [sg.HorizontalSeparator(color=colors["separator"])],
            [sg.Text("Description:", font=("Segoe UI", 11, "bold"),
                    text_color=colors["text"],
                    background_color=colors["background"])],
            [sg.Multiline(size=(60, 3), key="-DESCRIPTION-", 
                         disabled=True,
                         font=("Segoe UI", 10),
                         background_color=colors["code_bg"],
                         text_color=colors["text"],
                         border_width=1,
                         no_scrollbar=True)],
            [sg.Text("", background_color=colors["background"])],
            [sg.Text("Command:", font=("Segoe UI", 11, "bold"),
                    text_color=colors["text"],
                    background_color=colors["background"])],
            [sg.Input(size=(60, 1), key="-COMMAND-", 
                     disabled=True,
                     text_color=colors["code_text"],
                     font=("Consolas", 12, "bold"),
                     background_color=colors["code_bg"])],
            [sg.Button("📋 Copy Command", key="-COPY-", size=(18, 1),
                      font=("Segoe UI", 10, "bold"),
                      button_color=colors["button"]),
             sg.Button("☆ Add to Favorites", key="-ADD_FAV-", size=(18, 1),
                      font=("Segoe UI", 10),
                      button_color=colors["button"])],
            [sg.Text("", background_color=colors["background"])],
            [sg.Text("Notes:", font=("Segoe UI", 11, "bold"),
                    text_color=colors["text"],
                    background_color=colors["background"])],
            [sg.Multiline(size=(60, 4), key="-NOTES-", 
                         disabled=True,
                         font=("Segoe UI", 10),
                         background_color=colors["code_bg"],
                         text_color=colors["text"],
                         border_width=1,
                         no_scrollbar=True)],
            [sg.Text("", key="-STATUS-", 
                    text_color=colors["accent2"], 
                    font=("Segoe UI", 10, "italic"),
                    background_color=colors["background"],
                    size=(50, 1))]
        ]
        
        # Header
        header = [
            [sg.Text("🐧 Linux Beginner Assistant", 
                    font=("Segoe UI", 22, "bold"),
                    text_color=colors["title_color"],
                    background_color=colors["background"])],
            [sg.Text(f"Distribution: {self.data_manager.current_distribution}",
                    key="-DIST_NAME-", 
                    font=("Segoe UI", 11),
                    text_color=colors["subtitle_color"],
                    background_color=colors["background"])],
            [sg.Button("🔄 Change Distribution", key="-CHANGE_DIST-", size=(20, 1),
                      font=("Segoe UI", 10),
                      button_color=colors["button"]),
             sg.Text("  Theme:", 
                    font=("Segoe UI", 10),
                    text_color=colors["text"],
                    background_color=colors["background"]),
             sg.Combo(["Dark Gray", "Light Gray"], 
                     default_value=self.theme_manager.current_theme,
                     key="-THEME-",
                     enable_events=True,
                     size=(12, 1),
                     readonly=True,
                     font=("Segoe UI", 10),
                     background_color=colors["input"],
                     text_color=colors["input_text"],
                     button_background_color=colors["button"][1],
                     button_arrow_color=colors["button"][0])]
        ]
        
        # Main layout
        layout = [
            [sg.Column(header, justification='center', expand_x=True,
                      background_color=colors["background"],
                      element_justification='center')],
            [sg.HorizontalSeparator(color=colors["separator"])],
            [sg.Column(left_panel, vertical_alignment='top', 
                      background_color=colors["background"],
                      element_justification='left'),
             sg.VerticalSeparator(color=colors["separator"]),
             sg.Column(right_panel, vertical_alignment='top', expand_x=True,
                      background_color=colors["background"],
                      element_justification='left')]
        ]
        
        window = sg.Window(f"Linux Beginner Assistant - {self.data_manager.current_distribution}",
                        layout,
                        finalize=True,
                        resizable=True,
                        size=(1000, 680),
                        background_color=colors["background"],
                        margins=(10, 10))
        
        # Select first category and display first task if available
        if self.current_category and categories:
            window["-CATEGORIES-"].update(set_to_index=0)
            if tasks:
                window["-TASKS-"].update(set_to_index=0)
                self.update_task_display(window, tasks[0])
        
        return window
    
    def update_task_display(self, window: sg.Window, task: Dict[str, Any]) -> None:
        """
        Update the task display panel with selected task information.
        
        Args:
            window: PySimpleGUI Window object
            task: Task dictionary containing task information
        """
        if not task:
            return
            
        self.current_task = task
        colors = self.theme_manager.get_theme_colors()
        
        window["-TASK_TITLE-"].update(task.get("title", "No Title"))
        window["-DESCRIPTION-"].update(task.get("description", "No description available."))
        window["-COMMAND-"].update(task.get("command", ""))
        window["-NOTES-"].update(task.get("notes", "No additional notes."))
        window["-STATUS-"].update("")
        
        # Update favorite button
        if self.favorites_manager.is_favorite(task):
            window["-ADD_FAV-"].update("⭐ Remove from Favorites",
                                      button_color=(colors["favorite_color"], colors["button"][1]))
        else:
            window["-ADD_FAV-"].update("☆ Add to Favorites",
                                      button_color=colors["button"])
    
    def show_error_popup(self, message: str) -> None:
        """
        Show an error popup message.
        
        Args:
            message: Error message to display
        """
        colors = self.theme_manager.get_theme_colors()
        sg.popup(message, 
                title="Error", 
                icon='error',
                background_color=colors["background"],
                text_color=colors["text"],
                button_color=colors["button"])
    
    def show_info_popup(self, message: str) -> None:
        """
        Show an info popup message.
        
        Args:
            message: Info message to display
        """
        colors = self.theme_manager.get_theme_colors()
        sg.popup(message, 
                title="Information",
                background_color=colors["background"],
                text_color=colors["text"],
                button_color=colors["button"])
    
    def run(self) -> None:
        """Run the main application loop."""
        # Show welcome window
        welcome_window = self.create_welcome_window()
        main_window = None
        
        while True:
            window, event, values = sg.read_all_windows()
            
            # Handle window close events
            if event == sg.WIN_CLOSED:
                window.close()
                if window == main_window:
                    main_window = None
                    break
                elif window == welcome_window and not main_window:
                    break
                    
            # Handle Exit button
            elif event == "Exit":
                window.close()
                if window == main_window:
                    main_window = None
                    break
                elif window == welcome_window and not main_window:
                    break
                    
            # Welcome window events
            elif window == welcome_window:
                if event == "-THEME-":
                    self.theme_manager.set_theme(values["-THEME-"])
                    welcome_window.close()
                    welcome_window = self.create_welcome_window()
                    
                elif event == "-CONTINUE-":
                    if values["-DIST-"] and values["-DIST-"][0] != "No distributions found":
                        distribution = values["-DIST-"][0]
                        if self.data_manager.load_distribution_data(distribution):
                            welcome_window.close()
                            main_window = self.create_main_window()
                        else:
                            self.show_error_popup(
                                f"Failed to load data for {distribution}.\n\n"
                                "Please check if the data file exists in the 'data' folder.\n"
                                "File should be named: " + 
                                distribution.lower().replace(" ", "_") + ".json"
                            )
                    else:
                        self.show_error_popup(
                            "Please select a distribution first.\n\n"
                            "If no distributions are listed, make sure JSON files\n"
                            "are present in the 'data' folder."
                        )
            
            # Main window events
            elif window == main_window:
                if event == "-THEME-":
                    self.theme_manager.set_theme(values["-THEME-"])
                    # Recreate window with new theme
                    main_window.close()
                    main_window = self.create_main_window()
                    
                elif event == "-CHANGE_DIST-":
                    main_window.close()
                    main_window = None
                    welcome_window = self.create_welcome_window()
                    
                elif event == "-CATEGORIES-" and values["-CATEGORIES-"]:
                    self.showing_favorites = False
                    self.current_category = values["-CATEGORIES-"][0]
                    tasks = self.data_manager.get_tasks_by_category(self.current_category)
                    task_titles = [task["title"] for task in tasks]
                    
                    # Update tasks list
                    window["-TASKS-"].update(values=task_titles)
                    
                    # Display first task if available
                    if tasks:
                        window["-TASKS-"].update(set_to_index=0)
                        self.update_task_display(main_window, tasks[0])
                    else:
                        self.update_task_display(main_window, {
                            "title": "No tasks available",
                            "description": "No tasks found in this category.",
                            "command": "",
                            "notes": "Please select a different category."
                        })
                        
                elif event == "-TASKS-" and values["-TASKS-"]:
                    task_title = values["-TASKS-"][0]
                    if self.showing_favorites:
                        favorites = self.favorites_manager.get_all_favorites()
                        for task in favorites:
                            if task["title"] == task_title:
                                self.update_task_display(main_window, task)
                                break
                    else:
                        tasks = self.data_manager.get_tasks_by_category(self.current_category)
                        for task in tasks:
                            if task["title"] == task_title:
                                self.update_task_display(main_window, task)
                                break
                                
                elif event == "-SEARCH-":
                    query = values["-SEARCH-"]
                    if query:
                        results = self.data_manager.search_tasks(query)
                        if results:
                            task_titles = [task["title"] for task in results]
                            window["-TASKS-"].update(values=task_titles)
                            window["-CATEGORIES-"].update(set_to_index=[])
                            self.update_task_display(main_window, results[0])
                            self.showing_favorites = False
                        else:
                            window["-TASKS-"].update(values=[])
                            self.update_task_display(main_window, {
                                "title": "No results found",
                                "description": f"No tasks matching '{query}' were found.",
                                "command": "",
                                "notes": "Try a different search term."
                            })
                    else:
                        # Reset to current category when search is cleared
                        if self.current_category:
                            categories = self.data_manager.get_categories()
                            if self.current_category in categories:
                                idx = categories.index(self.current_category)
                                window["-CATEGORIES-"].update(set_to_index=idx)
                            tasks = self.data_manager.get_tasks_by_category(self.current_category)
                            task_titles = [task["title"] for task in tasks]
                            window["-TASKS-"].update(values=task_titles)
                            if tasks:
                                self.update_task_display(main_window, tasks[0])
                            
                elif event == "-FAVORITES-":
                    self.showing_favorites = True
                    favorites = self.favorites_manager.get_all_favorites()
                    if favorites:
                        fav_titles = [fav["title"] for fav in favorites]
                        window["-TASKS-"].update(values=fav_titles)
                        window["-CATEGORIES-"].update(set_to_index=[])
                        self.update_task_display(main_window, favorites[0])
                    else:
                        self.show_info_popup("No favorites added yet.\n\nClick '☆ Add to Favorites' to save commands you like.")
                        
                elif event == "-ALL_TASKS-":
                    self.showing_favorites = False
                    if self.current_category:
                        categories = self.data_manager.get_categories()
                        if self.current_category in categories:
                            idx = categories.index(self.current_category)
                            window["-CATEGORIES-"].update(set_to_index=idx)
                        tasks = self.data_manager.get_tasks_by_category(self.current_category)
                        task_titles = [task["title"] for task in tasks]
                        window["-TASKS-"].update(values=task_titles)
                        if tasks:
                            self.update_task_display(main_window, tasks[0])
                        
                elif event == "-COPY-":
                    if self.current_task and self.current_task.get("command"):
                        command = self.current_task.get("command", "")
                        if self.clipboard_manager.copy_to_clipboard(command):
                            window["-STATUS-"].update("✓ Command copied successfully!")
                        else:
                            window["-STATUS-"].update("✗ Failed to copy command")
                    else:
                        window["-STATUS-"].update("No command to copy")
                            
                elif event == "-ADD_FAV-":
                    if self.current_task and self.current_task.get("command"):
                        colors = self.theme_manager.get_theme_colors()
                        if self.favorites_manager.is_favorite(self.current_task):
                            self.favorites_manager.remove_favorite(self.current_task)
                            window["-ADD_FAV-"].update("☆ Add to Favorites",
                                                      button_color=colors["button"])
                            window["-STATUS-"].update("Removed from favorites")
                        else:
                            self.favorites_manager.add_favorite(self.current_task)
                            window["-ADD_FAV-"].update("⭐ Remove from Favorites",
                                                      button_color=(colors["favorite_color"], colors["button"][1]))
                            window["-STATUS-"].update("Added to favorites!")
                    else:
                        window["-STATUS-"].update("No task selected")
        
        if main_window:
            main_window.close()
        if welcome_window:
            welcome_window.close()
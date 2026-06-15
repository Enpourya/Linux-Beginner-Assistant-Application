#!/usr/bin/env python3
"""
Linux Beginner Assistant - Main Entry Point
A desktop application to help beginners learn Linux commands.
"""

import sys
from app import LinuxAssistantApp

def main():
    """Main function to start the Linux Beginner Assistant application."""
    try:
        app = LinuxAssistantApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
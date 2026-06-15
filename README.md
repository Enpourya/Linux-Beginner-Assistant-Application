# 🐧 Linux Beginner Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**A User-Friendly Desktop Application for Learning Linux Commands**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Architecture](#-architecture)

</div>

---

## 📖 Overview

**Linux Beginner Assistant** is a powerful yet user-friendly desktop application designed to bridge the gap between Linux newcomers and the command-line interface. Built with Python and PySimpleGUI, this application transforms the often intimidating world of Linux commands into an accessible, well-organized, and visually appealing learning experience.

The application serves as both a learning tool and a quick reference guide, providing carefully curated Linux commands across nine major distributions. Whether you're a student taking your first Linux course, a developer transitioning from Windows or macOS, or an IT professional needing a reliable command reference, this assistant streamlines your Linux learning journey.

---

## ✨ Features

### 🎯 Multi-Distribution Support
Covers **9 popular Linux distributions**, each with tailored commands for their specific package managers and system tools:

| Distribution | Package Manager | Type |
|-------------|----------------|------|
| **Ubuntu** | APT | Beginner-Friendly |
| **Debian** | APT-GET | Stable Foundation |
| **Fedora** | DNF | Cutting-Edge |
| **CentOS** | YUM | Enterprise Legacy |
| **Rocky Linux** | DNF | Enterprise Modern |
| **AlmaLinux** | DNF | Enterprise Alternative |
| **Arch Linux** | Pacman | Rolling Release |
| **Manjaro** | Pacman | User-Friendly Arch |
| **openSUSE** | Zypper | Enterprise-Ready |

### 📂 Organized Command Categories
Commands are logically grouped into **7 categories**:

| Category | Description | Example Commands |
|----------|------------|------------------|
| 🗂️ **File Management** | Navigate and manipulate filesystem | `ls`, `cp`, `mv`, `rm`, `mkdir` |
| 📦 **Package Management** | Install, remove, update software | `apt install`, `dnf update`, `pacman -S` |
| 👤 **User Management** | Manage system users and passwords | `useradd`, `passwd`, `userdel` |
| 💻 **System Information** | Monitor hardware and system status | `lscpu`, `free`, `df`, `uname` |
| 🌐 **Network** | Network configuration and troubleshooting | `ping`, `ip`, `ss`, `ifconfig` |
| ⚙️ **Process Management** | Control running processes | `ps`, `kill`, `htop`, `top` |
| 🔒 **Permissions** | Manage file security | `chmod`, `chown` |

### 🔍 Smart Search Functionality
Real-time search across all fields:
- Search by **task name** (e.g., "List Files")
- Search by **description** (e.g., "display files")
- Search by **command** (e.g., "ls -la")
- Results appear **dynamically** as you type

### ⭐ Favorites System
Build your personal command collection:
- **Save** frequently used commands with one click
- **Remove** commands you've memorized
- **View** all favorites in one place
- **Persistent** storage between sessions

### 📋 One-Click Clipboard
- Copy commands instantly with the **Copy Command** button
- Visual **confirmation** when copied
- **Time-saving** workflow integration

### 🎨 Dual Theme Support
| Theme | Background | Best For |
|-------|-----------|----------|
| 🌙 **Dark Gray** | `#2D2D2D` | Low-light environments, reduced eye strain |
| ☀️ **Light Gray** | `#F0F0F0` | Bright conditions, maximum readability |

### 📴 Complete Offline Operation
- All data stored **locally** in JSON files
- No **internet connection** required
- No **external API calls**
- Ideal for **secure environments**

### 🔧 Extensible Architecture
- **Modular design** for easy maintenance
- **JSON-based** data storage for simple updates
- **Scalable** structure for future features

---

## 🚀 Installation

### Prerequisites

- **Python 3.7** or higher
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Quick Install

```bash
# 1. Clone the repository (or download ZIP)
git clone https://github.com/yourusername/linux-beginner-assistant.git
cd linux-beginner-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

### Manual Install
```bash
# 1. Install PySimpleGUI
pip install PySimpleGUI

# 2. Install clipboard support
pip install pyperclip

# 3. Run the application
python main.py
```

### Project Structure

linux-beginner-assistant/
│
├── main.py                 # Application entry point
├── app.py                  # Main GUI and application logic
├── data_manager.py         # JSON data loading and querying
├── favorites_manager.py    # Favorites system with persistence
├── theme_manager.py        # Theme switching and management
├── clipboard_manager.py    # System clipboard operations
├── requirements.txt        # Python dependencies
├── README.md              # Documentation (this file)
│
├── data/                  # Command datasets (JSON files)
│   ├── ubuntu.json
│   ├── debian.json
│   ├── fedora.json
│   ├── centos.json
│   ├── rocky_linux.json
│   ├── almalinux.json
│   ├── arch_linux.json
│   ├── manjaro.json
│   └── opensuse.json
│
└── config/                # Application settings
    └── settings.json       # User preferences (theme, etc.)
	
### Left Panel - Navigation

┌─────────────────────┐
│  🔍 Search Bar      │  ← Type to search commands
├─────────────────────┤
│  Categories List    │  ← Click to filter by category
│  • File Management  │
│  • Package Mgmt     │
│  • User Management  │
│  • ...              │
├─────────────────────┤
│  Tasks List         │  ← Click to view task details
│  • List Files       │
│  • Copy Files       │
│  • Move Files       │
│  • ...              │
├─────────────────────┤
│ [⭐ Favorites]      │  ← View saved commands
│ [📋 Show All]       │  ← Show all tasks
└─────────────────────┘

### Right Panel - Task Details

┌──────────────────────────────────┐
│  Task Title                      │  ← Command name
├──────────────────────────────────┤
│  Description                     │  ← What it does
│  Explains the command purpose    │
├──────────────────────────────────┤
│  Command                         │  ← The actual command
│  $ ls -la                        │
├──────────────────────────────────┤
│  [📋 Copy Command]  [☆ Favorite] │  ← Action buttons
├──────────────────────────────────┤
│  Notes                           │  ← Tips & warnings
│  Important information here      │
├──────────────────────────────────┤
│  Status messages                 │  ← Confirmation
└──────────────────────────────────┘


### Design Philosophy

graph TB
    A[main.py] --> B[app.py]
    B --> C[data_manager.py]
    B --> D[favorites_manager.py]
    B --> E[theme_manager.py]
    B --> F[clipboard_manager.py]
    C --> G[JSON Data Files]
    D --> H[config/favorites.json]
    E --> I[config/settings.json]
# 📂 FileForge - Dynamic File Organizer

## 🚀 Project Overview

**FileForge** is a dynamic, GUI-based desktop application designed to automatically organize files in a specified folder. It reads file extensions, sorts them into customizable categories (like Images, Documents, Videos, etc.), and places them into corresponding, date-stamped subfolders.

This tool is perfect for keeping your Downloads folder or any active work directory clean and structured, either through a one-time operation or continuous real-time monitoring.

## ✨ Features

* **GUI Interface (Tkinter):** Simple and intuitive graphical user interface for easy interaction.
* **Customizable Categories:** File extensions for sorting are loaded from a **`categories.json`** configuration file, allowing you to easily edit and define your own file types.
* **Date-Based Sorting:** All moved files are organized into subfolders based on the **date of organization** (e.g., `Images/2025-10-03/filename.jpg`).
* **Real-Time Monitoring (Watchdog):** Can automatically monitor a folder and organize new files as soon as they are added (using threading for background watching).
* **Logging:** A **`fileforge_log.txt`** file is created to track every file movement, providing a clear history of all organizational actions.
* **"Others" Fallback:** Any file with an unknown extension is automatically moved to an **`Others`** folder, ensuring no file is left unorganized.

---

## 💻 Installation

### Prerequisites

You need **Python 3.x** installed on your system.

This project relies on a few external libraries. You can install all necessary dependencies using `pip`:

```bash
pip install watchdog
# Tkinter (for the GUI) is usually included with standard Python installations.

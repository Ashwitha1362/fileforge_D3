import os
import shutil
import threading
import json
from datetime import datetime
from tkinter import Tk, Label, Button, filedialog, Checkbutton, IntVar, messagebox, simpledialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ------------------ Config Files ------------------
CONFIG_FILE = "categories.json"
LOG_FILE = "fileforge_log.txt"

# Default categories if JSON does not exist
DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Others": []
}

# ------------------ Load or Create Categories ------------------
def load_categories():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CATEGORIES, f, indent=4)
        return DEFAULT_CATEGORIES
    else:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

FILE_CATEGORIES = load_categories()

# ------------------ Logging ------------------
def log_action(file_path, dest_path):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} : Moved '{file_path}' -> '{dest_path}'\n")

# ------------------ Core Organizer ------------------
def organize_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Get file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        moved = False
        for category, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                # Create date-based subfolder
                date_folder = datetime.now().strftime("%Y-%m-%d")
                category_folder = os.path.join(folder_path, category, date_folder)
                os.makedirs(category_folder, exist_ok=True)
                dest_path = os.path.join(category_folder, filename)
                shutil.move(file_path, dest_path)
                log_action(file_path, dest_path)
                moved = True
                break

        if not moved:
            # Move to Others if no match
            date_folder = datetime.now().strftime("%Y-%m-%d")
            other_folder = os.path.join(folder_path, "Others", date_folder)
            os.makedirs(other_folder, exist_ok=True)
            dest_path = os.path.join(other_folder, filename)
            shutil.move(file_path, dest_path)
            log_action(file_path, dest_path)

# ------------------ Watchdog Handler ------------------
class FileOrganizerHandler(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder

    def on_created(self, event):
        organize_files(self.folder)

    def on_modified(self, event):
        organize_files(self.folder)

# ------------------ GUI Application ------------------
class FileForgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📂 FileForge - College Version")
        self.root.geometry("600x350")

        self.folder_path = ""
        self.watch_mode = IntVar()
        self.observer = None

        # GUI Labels
        Label(root, text="📂 FileForge - Dynamic File Organizer", font=("Helvetica", 16)).pack(pady=10)
        Label(root, text="Select a folder to organize your files", font=("Helvetica", 12)).pack(pady=5)

        # Buttons
        Button(root, text="Select Folder", command=self.select_folder, width=25).pack(pady=5)
        Button(root, text="Organize Files Now", command=self.organize_now, width=25).pack(pady=5)
        Checkbutton(root, text="Auto Watch Folder", variable=self.watch_mode, command=self.toggle_watch).pack(pady=5)
        Button(root, text="Edit Categories", command=self.edit_categories, width=25).pack(pady=5)

        # Status Label
        self.status_label = Label(root, text="Status: Waiting for folder selection", fg="blue")
        self.status_label.pack(pady=10)

        Label(root, text="Advanced Features: Date-based folders, logging, editable categories", fg="green").pack(pady=5)

    # ------------------ GUI Functions ------------------
    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path = folder_selected
            self.status_label.config(text=f"Selected Folder: {self.folder_path}", fg="green")

    def organize_now(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        organize_files(self.folder_path)
        self.status_label.config(text="✅ Files organized successfully!", fg="green")

    def toggle_watch(self):
        if self.watch_mode.get():
            if not self.folder_path:
                messagebox.showwarning("Warning", "Please select a folder first!")
                self.watch_mode.set(0)
                return
            self.start_watch()
            self.status_label.config(text="👀 Watching folder for new files...", fg="orange")
        else:
            self.stop_watch()
            self.status_label.config(text="Stopped watching folder.", fg="red")

    def start_watch(self):
        if self.observer:
            self.stop_watch()
        event_handler = FileOrganizerHandler(self.folder_path)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.folder_path, recursive=False)
        self.observer_thread = threading.Thread(target=self.observer.start, daemon=True)
        self.observer_thread.start()

    def stop_watch(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

    def edit_categories(self):
        # Simple GUI to edit categories inside app
        global FILE_CATEGORIES
        for category in FILE_CATEGORIES:
            ext_string = ",".join(FILE_CATEGORIES[category])
            new_ext = simpledialog.askstring("Edit Category", f"Extensions for '{category}' (comma separated):", initialvalue=ext_string)
            if new_ext is not None:
                FILE_CATEGORIES[category] = [e.strip() for e in new_ext.split(",") if e.strip()]

        # Save to JSON
        with open(CONFIG_FILE, "w") as f:
            json.dump(FILE_CATEGORIES, f, indent=4)
        messagebox.showinfo("Success", "Categories updated successfully!")

# ------------------ Run App ------------------
if __name__ == "__main__":
    root = Tk()
    app = FileForgeApp(root)
    root.mainloop()

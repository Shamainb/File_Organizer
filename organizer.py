
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess  # For running PowerShell commands

# File types categorized
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico', '.heic', '.raw'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.xls', '.ppt', '.pptx', '.epub', '.md', '.csv'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.webm'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.iso', '.bz2'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.c', '.cpp', '.json', '.xml', '.php', '.go', '.ts', '.sh', '.bat', '.rb'],
    'Executables': ['.exe', '.msi', '.bat', '.sh', '.app', '.apk', '.deb', '.dmg'],
    'Fonts': ['.ttf', '.otf', '.woff', '.woff2'],
    'Disk Images': ['.iso', '.img', '.vdi', '.vmdk', '.dmg']
}

# Function to categorize files based on type
def categorize_file(filename):
    extension = os.path.splitext(filename)[1]
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

# Main organizing function
def organize_files(folder_path, preview_only=False):
    organized = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            # Get the category of the file
            category = categorize_file(filename)
            target_folder = os.path.join(folder_path, category)
            
            if preview_only:
                organized[filename] = category
            else:
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                shutil.move(file_path, os.path.join(target_folder, filename))
    
    return organized

# Function to remove files from Desktop after organizing
def organize_and_remove_from_desktop():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    organize_files(desktop_path)
    
    # Refresh Desktop after organizing
    refresh_desktop()

# Function to refresh the Desktop using PowerShell
def refresh_desktop():
    try:
        # Use PowerShell to refresh Desktop icons
        command = 'powershell.exe -Command "ie4uinit.exe -ClearIconCache; Stop-Process -Name explorer; Start-Process explorer"'
        subprocess.run(command, shell=True)
        print("Desktop refreshed successfully.")
    except Exception as e:
        print(f"Error refreshing Desktop: {e}")

# GUI Application class
class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x400")
        
        # Path label and button to select a folder
        self.label = tk.Label(root, text="Select Folder to Organize")
        self.label.pack(pady=10)
        
        self.folder_path = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.folder_path, width=50)
        self.entry.pack(pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)
        
        # Text box to preview the file organization
        self.preview_text = ScrolledText(root, height=10, width=70)
        self.preview_text.pack(pady=10)
        
        # Buttons to preview and organize files
        self.preview_button = tk.Button(root, text="Preview", command=self.preview_files)
        self.preview_button.pack(pady=5)

        self.organize_button = tk.Button(root, text="Organize Files and Clear Desktop", command=self.organize_and_remove_files)
        self.organize_button.pack(pady=5)
    
    # Browse for folder
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
    
    # Preview files to be organized
    def preview_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder to organize.")
            return
        
        organized = organize_files(folder, preview_only=True)
        
        # Clear preview text box and display organization plan
        self.preview_text.delete(1.0, tk.END)
        if organized:
            for filename, category in organized.items():
                self.preview_text.insert(tk.END, f"{filename} -> {category}\n")
        else:
            self.preview_text.insert(tk.END, "No files to organize.\n")
    
    # Organize files into folders and remove from Desktop
    def organize_and_remove_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder to organize.")
            return
        
        if messagebox.askyesno("Confirm Organization", "Are you sure you want to organize the files?"):
            organize_files(folder)
            organize_and_remove_from_desktop()  # Organize Desktop files too
            messagebox.showinfo("Success", "Files have been organized successfully!")
            self.preview_text.delete(1.0, tk.END)  # Clear preview after organizing
            
            # Refresh Desktop after clearing
            refresh_desktop()
            messagebox.showinfo("Desktop Cleanup", "Files from Desktop have been organized and Desktop refreshed.")

# Create the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
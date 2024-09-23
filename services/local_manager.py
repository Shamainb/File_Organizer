import os
import shutil

def organize_local_files():
    base_directory = 'uploads/'
    
    for filename in os.listdir(base_directory):
        file_path = os.path.join(base_directory, filename)
        
        if os.path.isfile(file_path):
            extension = filename.split('.')[-1].lower()
            folder = categorize_extension(extension)
            
            target_folder = os.path.join(base_directory, folder)
            os.makedirs(target_folder, exist_ok=True)
            
            shutil.move(file_path, os.path.join(target_folder, filename))

def categorize_extension(extension):
    if extension in ['jpg', 'jpeg', 'png', 'gif']:
        return 'Images'
    elif extension in ['txt', 'pdf']:
        return 'Documents'
    elif extension in ['mp4', 'mkv']:
        return 'Videos'
    else:
        return 'Others'

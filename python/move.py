import os
import shutil

# Define the source and destination directories
source_dir = 'anime_characters'
destination_dir = 'new_folder'

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Walk through the directory tree
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Check if the file is a .jpg image
        if file.endswith('.jpg'):
            # Construct the full path of the source file
            source_path = os.path.join(root, file)
            # Construct the full path of the destination file
            destination_path = os.path.join(destination_dir, file)
            
            # Move the file
            shutil.move(source_path, destination_path)
            print(f"Moved: {source_path} to {destination_path}")

print("All images have been moved.")
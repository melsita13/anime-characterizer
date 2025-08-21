import os

def rename_and_log_images(base_folder_path, log_file_name="renamed_images.txt"):
    """
    Renames the first image file in each subfolder of a given base folder
    and logs the changes to a text file.
    """
    if not os.path.isdir(base_folder_path):
        print(f"Error: The base folder '{base_folder_path}' does not exist.")
        return

    # Use 'w' mode to create a new log file or overwrite an existing one
    with open(log_file_name, 'w', encoding='utf-8') as log_file:
        print("Starting the renaming process and logging to 'renamed_images.txt'...")
        log_file.write("Original Name -> New Name\n")
        log_file.write("--------------------------\n")

        for folder_name in os.listdir(base_folder_path):
            folder_path = os.path.join(base_folder_path, folder_name)

            if os.path.isdir(folder_path):
                print(f"\nProcessing folder: {folder_name}")

                for file_name in os.listdir(folder_path):
                    original_file_path = os.path.join(folder_path, file_name)

                    if os.path.isfile(original_file_path):
                        # Get the parent folder name and remove the leading underscore
                        new_name = folder_name.strip('_')
                        
                        # Get the file extension
                        file_extension = os.path.splitext(file_name)[1]
                        
                        # Create the new file path
                        new_file_path = os.path.join(folder_path, f"{new_name}{file_extension}")

                        # Rename the file and log the action
                        try:
                            os.rename(original_file_path, new_file_path)
                            log_entry = f"{file_name} -> {os.path.basename(new_file_path)}\n"
                            log_file.write(log_entry)
                            print(f"  ✅ Renamed '{file_name}' to '{os.path.basename(new_file_path)}'")
                        except Exception as e:
                            print(f"  ❌ Failed to rename '{file_name}': {e}")
                            log_file.write(f"Error renaming '{file_name}': {e}\n")
                        
                        # Stop after renaming the first file in the folder
                        break 
                else:
                    print(f"  ⚠️ No files found in '{folder_name}'.")

    print("\nProcess finished. Check 'renamed_images.txt' for the log of changes.")

# Example Usage (create dummy directories and files for demonstration)
base_folder = 'anime_characters'

os.makedirs('anime_characters/_Kaseka', exist_ok=True)
os.makedirs('anime_characters/_Kuniki', exist_ok=True)
os.makedirs('anime_characters/_Lupin_III', exist_ok=True)
os.makedirs('anime_characters/_Sakaki', exist_ok=True)

with open('anime_characters/_Kaseka/image.jpg', 'w') as f: f.write('dummy')
with open('anime_characters/_Kuniki/dummy.png', 'w') as f: f.write('dummy')
with open('anime_characters/_Lupin_III/another_image.jpeg', 'w') as f: f.write('dummy')
with open('anime_characters/_Sakaki/pic.gif', 'w') as f: f.write('dummy')

# Run the function
rename_and_log_images(base_folder)

# Clean up the dummy folders and files after the script runs
for dir_path in ['anime_characters/_Kaseka', 'anime_characters/_Kuniki', 'anime_characters/_Lupin_III', 'anime_characters/_Sakaki']:
    try:
        for file_name in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file_name))
        os.rmdir(dir_path)
    except OSError as e:
        print(f"Error during cleanup: {e}")
try:
    os.remove('renamed_images.txt')
    os.rmdir(base_folder)
except OSError as e:
    print(f"Error during cleanup: {e}")
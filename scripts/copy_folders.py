import os
import shutil
import sys

def copy_items(src_folder, dest_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    # Iterate through items in the source folder
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)

        # Copy the item to the destination folder
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, symlinks=False, ignore=None)

def main():
    # Prompt the user for folder paths
    has_true = input("Enter the path of the True folder: ")
    has_false = input("Enter the path of the False folder: ")

    # Command-line arguments for source folders and destination folder
    true_folder = sys.argv[1]
    false_folder = sys.argv[2]

    # Copy items from the first folder
    copy_items(has_true, true_folder)

    # Copy items from the second folder
    copy_items(has_false, false_folder)
   
    print(f"\nItems copied to destination folders")

if __name__ == "__main__":
    main()

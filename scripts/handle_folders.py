import cv2
import os
import shutil
import sys

def rename_files(folder_path, new_prefix):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate through each file and rename it
    for i, filename in enumerate(files, start=1):
        old_path = os.path.join(folder_path, filename)
        
        # Create a new filename with the specified prefix and a number
        new_filename = f"{new_prefix}_{i}.png"
        
        # Construct the new path for the file
        new_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_path, new_path)
        
        print(f"Renamed: {filename} to {new_filename}")

def resize_images(base_folder, image_size):
    # Check if the base folder path exists
    if not os.path.exists(base_folder):
        print(f"The folder '{base_folder}' does not exist.")
        return
    
    # Iterate through each folder and subfolder in the base folder
    for folder_name, _, files in os.walk(base_folder):
        for filename in files:
            file_path = os.path.join(folder_name, filename)
            
            # Open the image file
            try:
                image = cv2.imread(file_path)
            except Exception as e:
                print(f"Error opening {filename}: {e}")
                continue

            # Determine the dimensions of the box (the shorter side)
            x_img, y_img = image.shape[1], image.shape[0]
            box_size = min(x_img, y_img)

            # Calculate the coordinates for cropping to a square
            left = (x_img - box_size) // 2
            top = (y_img - box_size) // 2
            right = left + box_size
            bottom = top + box_size

            # Crop the image to the calculated square
            cropped_image = image[top:bottom, left:right]

            # Resize the cropped image to the desired size
            resized_image = cv2.resize(cropped_image, (int(image_size), int(image_size)), interpolation=cv2.INTER_AREA)

            # Save the resized image
            cv2.imwrite(file_path, resized_image)
            print(f"resized {filename}")


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
    print("Make sure the folders don't contain images using the 'false_number' or 'true_number' format")

    has_true = input("Enter the path of the True folder: ")
    has_false = input("Enter the path of the False folder: ")

    # Command-line arguments for source folders and destination folder
    true_folder = sys.argv[1]
    false_folder = sys.argv[2]

    if int(sys.argv[3]) >= 130:
        image_size = sys.argv[3]
    else: 
        image_size = 130

    # Copy items from the first folder
    copy_items(has_true, true_folder)

    # Copy items from the second folder
    copy_items(has_false, false_folder)

    rename_files(true_folder, "t")
    rename_files(false_folder, "f")

    # Call the function to resize images
    resize_images(true_folder, image_size)
    resize_images(false_folder, image_size)
   
    print(f"\nItems copied to destination folders")

if __name__ == "__main__":
    main()

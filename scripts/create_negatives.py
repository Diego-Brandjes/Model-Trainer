import os
import sys

def write_image_filenames_to_txt(folder_path, output_txt):
    # Get a list of all image filenames in the folder
    image_filenames = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

    # Write image filenames to the output text file
    with open(output_txt, 'w') as txt_file:
        for filename in image_filenames:
            txt_file.write(filename + '\n')

def count_files_in_folder(folder_path):
    # Count the number of files in the folder
    file_count = len([file for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg', '.JPG'))])
    return file_count

if __name__ == "__main__":
    # Specify the folder path and output text file
    folder_path = sys.argv[1]
    output_txt = sys.argv[2]

    # Call the function to write image filenames to the text file
    write_image_filenames_to_txt(folder_path, output_txt)

    # Count files and write the count to negative_amount.tmp
    file_count = count_files_in_folder(folder_path)
    with open("negative_amount.tmp", 'w') as count_file:
        count_file.write(str(file_count))

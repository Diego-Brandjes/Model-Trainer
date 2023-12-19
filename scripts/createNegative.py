import os
import sys

def write_image_filenames_to_txt(folder_path, output_txt):
    # Get a list of all image filenames in the folder
    image_filenames = [os.path.join('no_faces', file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

    # Write image filenames to the output text file
    with open(output_txt, 'w') as txt_file:
        for filename in image_filenames:
            txt_file.write(filename + '\n')

if __name__ == "__main__":
    # Specify the folder path and output text file
    folder_path = sys.argv[1]
    output_txt = sys.argv[2]

    # Call the function to write image filenames to the text file
    write_image_filenames_to_txt(folder_path, output_txt)

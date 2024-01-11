import subprocess
import requests
import os
import sys


# WINDOWS INSTALLER
def check_opencv_installed():
    try:
        # Attempt to import OpenCV
        import cv2
        print("OpenCV is already installed.")
        return True
    except ImportError:
        print("OpenCV is not present or installed correctly.")
        return False

def add_opencv_to_path(opencv_path):
    try:
        # Get the current PATH variable
        current_path = os.environ.get('PATH', '')

        # Add the OpenCV bin directory to the PATH
        opencv_bin_path = os.path.join(opencv_path, 'build', 'x64', 'vc15', 'bin')
        new_path = f"{current_path};{opencv_bin_path}"

        # Update the PATH variable
        os.environ['PATH'] = new_path

        print(f"Added {opencv_bin_path} to the PATH.")

    except Exception as e:
        print(f"Error adding OpenCV to PATH: {e}")

def install_requirements():
    try:
        if not check_opencv_installed():
            # URL of the OpenCV installer
            opencv_url = "https://sourceforge.net/projects/opencvlibrary/files/3.4.16/opencv-3.4.16-vc14_vc15.exe/download"

            # Download the file
            response = requests.get(opencv_url)
            with open("opencv_installer.exe", "wb") as file:
                file.write(response.content)

            # Run the installer
            subprocess.run(["opencv_installer.exe"])


            # Add OpenCV to the PATH
            add_opencv_to_path(os.getcwd())

            print("OpenCV installed successfully.")
        else:
            print("Skipping OpenCV installation as it is already installed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    install_requirements()

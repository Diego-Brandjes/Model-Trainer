import subprocess
import requests
import os
import ctypes
import sys
from pathlib import Path

# WINDOWS INSTALLER
def check_opencv_installed():

    path = input("Provide the opencv folder path, leave empty if opencv is not installed:\n")

    if path == None or path == "":
        print("No path supplied, proceeding to download opencv...")
        return False
    else:
        try:
            opencv_path = os.path.join(path, 'build', 'x64', 'vc15', 'bin')
            print(opencv_path)
            add_opencv_to_path(opencv_path)

            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
            subprocess.run("opencv_version", shell=True, check=True)
            return True
        
        except subprocess.CalledProcessError:
            print("OpenCV is not present or installed correctly.")
            return False


def add_opencv_to_path(opencv_path):
    try:
        # Get the current PATH variable
        current_path = os.environ.get('PATH', '')

        # Append the OpenCV bin directory to the PATH with the correct separator
        new_path = f"{current_path}{os.pathsep}{opencv_path}"

        # Update the PATH variable
        os.environ['PATH'] = new_path

        print(f"Added {opencv_path} to the PATH.")

    except Exception as e:
        print(f"Error adding OpenCV to PATH: {e}")


def install_opencv():
    # URL of the OpenCV installer
    opencv_url = "https://sourceforge.net/projects/opencvlibrary/files/3.4.16/opencv-3.4.16-vc14_vc15.exe"
    download_folder = str(Path.home() / "Downloads")

    print("Downloading OpenCV...")
    # Download the file to the download folder
    response = requests.get(opencv_url)
    with open(os.path.join(download_folder, "opencv_installer.exe"), "wb") as file:
        file.write(response.content)

    print("Running OpenCV installer...")
    # Run the installer
    subprocess.run([os.path.join(download_folder, "opencv_installer.exe")])

    path = input("Provide the opencv folder path.\n")

    if path == None:
        print("No path supplied, please add it manually...")
    else:
        opencv_path = os.path.join(path, 'build', 'x64', 'vc15', 'bin')
        add_opencv_to_path(opencv_path)


def install_requirements():

    try:
        if not check_opencv_installed():
            install_opencv()
            print("OpenCV installed successfully.")

        else:
            print("OpenCV is already installed.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        input("Press enter to close installer.")

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() != 1:
        # Re-run the script with elevated privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        install_requirements()
import subprocess
import requests

def check_opencv_installed():
    try:
        # Attempt to import OpenCV
        import cv2
        print("OpenCV is already installed.")
        return True
    except ImportError:
        print("OpenCV is not present or installed correctly.")
        return False

def install_requirements():
    try:          
        # Install the required packages using pip
        subprocess.check_call(['pip', 'install', 'opencv-python'])

        print("All required packages installed successfully.")

        if not check_opencv_installed():
            # URL of the OpenCV installer
            opencv_url = "https://sourceforge.net/projects/opencvlibrary/files/3.4.16/opencv-3.4.16-vc14_vc15.exe/download"

            # Download the file
            response = requests.get(opencv_url)
            with open("opencv_installer.exe", "wb") as file:
                file.write(response.content)

            # Run the installer
            subprocess.run(["opencv_installer.exe"])

            print("OpenCV installed successfully.")
        else:
            print("Skipping OpenCV installation as it is already installed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    install_requirements()

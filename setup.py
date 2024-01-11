import subprocess
import requests
import zipfile
import io
import os
import sys

# INSTALLER FOR UNIX SYSTEMS
def check_opencv_installed():
    try:
        subprocess.run("opencv_version", shell=True, check=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])

        print("OpenCV is already installed.")
        return True
    
    except subprocess.CalledProcessError:
            print("OpenCV is not present or installed correctly.")
            return False

def install_requirements():
    try:
        if not check_opencv_installed():
            # URL of the OpenCV zip file
            opencv_url = "https://github.com/opencv/opencv/archive/3.4.16.zip"

            # Download the file
            response = requests.get(opencv_url)
            
            # Extract the contents of the ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
                zip_ref.extractall("opencv")

            print("OpenCV extracted successfully.")

            # Build and install OpenCV
            opencv_source_dir = os.path.join("opencv", "opencv-3.4.16")
            opencv_build_dir = os.path.join(opencv_source_dir, "build")

            os.makedirs(opencv_build_dir, exist_ok=True)
            subprocess.run(["cmake", opencv_source_dir], cwd=opencv_build_dir)
            subprocess.run(["make"], cwd=opencv_build_dir)
            subprocess.run(["sudo", "make", "install"], cwd=opencv_build_dir)

            print("OpenCV installed successfully.")
        else:
            print("Skipping OpenCV installation as it is already installed.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        input("Press enter to close the installer")

if __name__ == "__main__":
    install_requirements()
    

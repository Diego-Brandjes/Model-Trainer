## Python scripts

### check_image
This file will run the script that will check images supplied in the 'input' folder

### confirm_positives
Will ask the user to input the value the VEC bash script displays to correctly identify the amount of positive samples, as they can be higher than the amount of supplied images.

The amount will be saved to a .tmp file which is read in the makefile later on.

### copy_folder
This script will ask the user to supply two folders for images, eg. a folder with images of faces and one with pictures without faces.

They will be copied to a local folder so the OpenCV bash script can access them. 

*note: these folders will be deleted after the training is finished.*

### create_negatives

This script will count up all the files places in the negative image folder. This number will be saved to a .tmp file and again is accessed later on in the makefile.

### webcam
Will run the webcam on the device, if present. After the .xml is created this script will show the deteced area on the camera view by drawing a green box around the area that matches with the .xml model.



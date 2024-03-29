# Image Recognition Model Trainer (IRMT)


## Dependencies
- OpenCV ^3.4.16
- Python ^3.11.7
- GNU Make 3.82.90

## Package installer

I also included a simple setup file that will download the required files. OpenCV requires some tinkering to work on windows devices by placing the bin in the windows environment variables.

```
# Requires pip!
python3 setup.py    
```
## Example

Here is an example of the included .xml trained using 263 positive and 387 negative pictures.

### Using the created model
![Alt text](https://i.ibb.co/zRLS0j6/pc.png "Using the created xml")

### Using the standard opencv model
![Alt text](https://i.ibb.co/PhP9N1w/opencv.png "Using the OpenCV")

TP meaning true postives,

FP meaning false positives,

FN meaning false negatives

## Training
- Please run the following command:
```
make train
```
This will open the program in the command line and promt you to enter two filepaths to image folders.

After entering these folders they will be checked and trained upon. 

The user has to enter the amount of samples the VEC file shows in the command line.

```
VEC CREATED
Confirm sample count
python scripts/confirm_samples.py
CONFIRM SAMPLES: <user input here>
```

After this is done the user can wait until the cascade.xml is finished.

## Detection

The user can run included extra scripts using

```
make detect
make webcam
```
### Detect 
Will require the user to place images into the folder "input" which was created after the model is finished. The output folder will show the images with detection boxes. The images will also pop up on the screen and will disappear on a keypress.

### Webcam 
Will activate the webcam using python, this only works when the device has a webcam and is still unstable at this point. If the webcam does work it will show a green detection box if it found similarities.

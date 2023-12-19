import cv2
import os
import sys

def capture_images(output_folder, num_images):
    # Open a connection to the webcam (0 represents the default webcam)
    cap = cv2.VideoCapture(0)

    # Set the camera frame size to 300x300
    cap.set(3, 160)  # 3 corresponds to CV_CAP_PROP_FRAME_WIDTH
    cap.set(4, 120)  # 4 corresponds to CV_CAP_PROP_FRAME_HEIGHT

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # Loop to capture images
        for i in range(num_images):
            # Read a frame from the webcam
            ret, frame = cap.read()

            # Display the frame (optional)
            cv2.imshow('camera', frame)

            # Save the image with a numbered filename
            image_name = os.path.join(output_folder, f'image_{i+1}.png')
            cv2.imwrite(image_name, frame)

            # Pause briefly (optional)
            cv2.waitKey(100)

    finally:
        # Release the webcam and close any open windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Specify the output folder and the number of images to capture
    if len(sys.argv) != 3:
        print("Usage: python script.py <output_folder> <num_images>")
        sys.exit(1)

    output_folder = sys.argv[1]
    num_images = int(sys.argv[2])

    # Capture images
    capture_images(output_folder, num_images)

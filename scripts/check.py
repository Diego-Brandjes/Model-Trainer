import os
import cv2
import sys

# Input and output paths
input_folder = sys.argv[1]  # Replace with the path to your input folder
output_folder = sys.argv[2]  # Replace with the path to your output folder

# Initialize the classifier
cascade = cv2.CascadeClassifier()
cascade.load('xml\\cascade.xml')

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is an image (you may want to add more file format checks)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Load the image from file
        image_path = os.path.join(input_folder, filename)
        frame = cv2.imread(image_path)

        # Check if the image is loaded correctly
        if frame is None:
            print(f"Cannot open image at {image_path}")
            continue

        # Rescale the image to 160x120
        rescaled_frame = cv2.resize(frame, (160, 120))

        # Convert the rescaled image to grayscale
        gray = cv2.cvtColor(rescaled_frame, cv2.COLOR_BGR2GRAY)

        # Draw rectangles around the detected faces
        faces = cascade.detectMultiScale(gray, minNeighbors=10)
        for (x, y, w, h) in faces:
            cv2.rectangle(rescaled_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Calculate the scaling factor to maintain aspect ratio
        max_size = 500
        aspect_ratio = rescaled_frame.shape[1] / rescaled_frame.shape[0]
        new_width = min(max_size, int(max_size * aspect_ratio))
        new_height = min(max_size, int(max_size / aspect_ratio))

        # Upscale the image while maintaining aspect ratio
        upscaled_frame = cv2.resize(rescaled_frame, (new_width, new_height))

        # Save the image with rectangles drawn around faces to the output folder
        output_path = os.path.join(output_folder, f'output_{filename}')
        cv2.imwrite(output_path, upscaled_frame)

        print(f"Image saved to {output_path}")

# Display the saved images (optional)
for filename in os.listdir(output_folder):
    saved_image_path = os.path.join(output_folder, filename)
    saved_image = cv2.imread(saved_image_path)
    cv2.imshow(f'Saved Image: {filename}', saved_image)
    cv2.waitKey(0)

cv2.destroyAllWindows()
import os
import cv2

# Input and output paths
input_folder = 'input/'  # Replace with the path to your input folder
output_folder = 'output/'  # Replace with the path to your output folder

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
            # Create a new image with only the region inside the detected face bounding box
            face_image = rescaled_frame[y:y+h, x:x+w]

            # Add a green border to the face image
            border_color = (0, 255, 0)  # Green color
            border_size = 2
            face_image_with_border = cv2.copyMakeBorder(face_image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)

            # Resize the image to a width of 500 and scale the height accordingly
            scale_factor = 500 / face_image_with_border.shape[1]
            new_width = 500
            new_height = int(face_image_with_border.shape[0] * scale_factor)
            face_image_with_border_resized = cv2.resize(face_image_with_border, (new_width, new_height))

            # Save the resized face image with a green border to the output folder
            output_path = os.path.join(output_folder, f'output_{filename}')
            cv2.imwrite(output_path, face_image_with_border_resized)
            print(f"Resized face with border saved to {output_path}")

# Display the saved face images with borders (optional)
for filename in os.listdir(output_folder):
    saved_face_path = os.path.join(output_folder, filename)
    saved_face_with_border_resized = cv2.imread(saved_face_path)

    # Check if the image is loaded correctly
    if saved_face_with_border_resized is None:
        print(f"Cannot open saved image at {saved_face_path}")
        continue

    cv2.imshow(f'Saved Resized Face with Border: {filename}', saved_face_with_border_resized)
    cv2.waitKey(0)

cv2.destroyAllWindows()

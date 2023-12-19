import cv2

# Initialize the Camera
camera = cv2.VideoCapture(0)

codec = 0x47504A4D  # MJPG
camera.set(cv2.CAP_PROP_FPS, 60.0)
camera.set(cv2.CAP_PROP_FOURCC, codec)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 90)

# Initialize the classifier
cascade = cv2.CascadeClassifier()
cascade.load('xml\\cascade.xml')

# Check if the webcam is opened correctly
if not camera.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Draw rectangles around the detected faces
    faces = cascade.detectMultiScale(gray, minNeighbors=16)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        break

    cv2.imshow('Input', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break

camera.release()
cv2.destroyAllWindows()
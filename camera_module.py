# camera_module.py
import cv2

def capture_iris_image(filename):
    cap = cv2.VideoCapture(0)  # Or your NIR camera
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
        cv2.imshow("Captured Iris", frame)  # Display the captured image
        cv2.waitKey(0)  # Wait for a key press
        cv2.destroyAllWindows()
    cap.release()
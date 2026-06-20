# activity_detection.py
import cv2
import mediapipe as mp
import numpy as np
import threading

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def eye_aspect_ratio(landmarks, left_eye_indices, right_eye_indices):
    def calculate_ear(eye_landmarks):
        A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
        B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
        C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
        return (A + B) / (2.0 * C)

    left_eye_landmarks = [[landmarks[i].x, landmarks[i].y] for i in left_eye_indices]
    right_eye_landmarks = [[landmarks[i].x, landmarks[i].y] for i in right_eye_indices]

    left_ear = calculate_ear(left_eye_landmarks)
    right_ear = calculate_ear(right_eye_landmarks)
    return (left_ear + right_ear) / 2.0

def detect_eye_closure(frame, ear_threshold=0.2):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        left_eye_indices = [362, 382, 381, 380, 374, 373]
        right_eye_indices = [33, 7, 163, 144, 145, 153]
        ear = eye_aspect_ratio(landmarks, left_eye_indices, right_eye_indices)

        print(f"EAR: {ear}")

        if ear < ear_threshold:
            return "Eyes Closed"
        else:
            return "Eyes Open"
    else:
        return "No Face Detected"

def run_detection(result_queue, stop_event, ear_threshold=0.2):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        result_queue.put("Error: Could not open camera.")
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            result_queue.put("Error: Could not read frame.")
            break

        eye_status = detect_eye_closure(frame, ear_threshold)
        result_queue.put(eye_status)

        cv2.putText(frame, eye_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Eye Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
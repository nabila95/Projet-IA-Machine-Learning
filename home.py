import streamlit as st
import cv2
import dlib
import cvlib as cv
import numpy as np


st.title("Emotion Detection App")

# Load the pre-trained facial landmark predictor for face detection
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Create a function to capture video from the webcam
def capture_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            # Iterate through detected faces and detect emotions
            for face in faces:
                x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
                cropped_face = frame[y1:y2, x1:x2]
                emotion_label, _ = cv.detect_emotion(cropped_face)
                cv2.putText(frame, emotion_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Display the frame with emotion labels
            st.image(frame, channels="BGR")

    cap.release()
    cv2.destroyAllWindows()

if st.button("Start Emotion Detection"):
    capture_video()

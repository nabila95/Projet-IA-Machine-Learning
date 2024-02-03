import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

# Load the emotion detection model
classifier = load_model('model.h5')  # Update the path to where your model is located

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Create a Streamlit app
st.title("Emotion Detection App")

# Initialize the label variable
label = "No Faces Detected"  # Default value
accuracy = 0.0  # Initialize accuracy variable

# User uploads an image
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                predictions = classifier.predict(roi)
                max_index = np.argmax(predictions[0])
                label = emotion_labels[max_index]
                accuracy = round(predictions[0][max_index] * 100, 2)  # Calculate accuracy
                label_position = (x, y)
                cv2.putText(image, f"{label} {accuracy}%", label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the processed image
        st.image(image, channels="BGR", use_column_width=True)
        st.write(f"Emotion Detected: {label} with {accuracy}% accuracy")
    else:
        st.write("No faces detected.")

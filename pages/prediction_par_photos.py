import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
from PIL import Image

# Charger le modèle de détection d'émotion
classifier = load_model('model.h5')  # Assurez-vous que le chemin vers votre modèle est correct
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

st.title("Application de détection d'émotion")

# Fonction pour prédire l'émotion
def predict_emotion(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        roi = roi_gray.astype('float') / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        
        prediction = classifier.predict(roi)[0]
        emotion = emotion_labels[prediction.argmax()]
        return emotion, prediction.max()

# Capture de l'image depuis la webcam
uploaded_file = st.camera_input("Prenez une photo")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image capturée', use_column_width=True)
    
    # Prédiction de l'émotion
    emotion, confidence = predict_emotion(image)
    st.write(f"Émotion détectée: {emotion} avec une confiance de {confidence:.2f}%")

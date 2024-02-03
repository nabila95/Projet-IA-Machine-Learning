import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

# charger le model
classifier = load_model(r'C:/Users/Muthuvel/OneDrive - Ecole IPSSI/M2/Intelligence artificielle - Machine learning/Projet/model.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']


st.title("Emotion Detection App")

# Initialize the label variable
label = "No Faces"  # valueur par défaut

# Open the webcam
cap = cv2.VideoCapture(0)

# Ce script utilise OpenCV pour capturer le flux vidéo d'une webcam, détecter les visages dans l'image en temps réel,
# et prédire leur émotion à l'aide d'un modèle pré-entraîné. Les résultats sont affichés dans une application Streamlit.

if not cap.isOpened():
    st.error("Error: Could not access the webcam.")  # Affiche une erreur si la webcam n'est pas accessible
else:
    ret, frame = cap.read()  # Lit une image de la vidéo
    if ret:
        labels = []  # Liste pour stocker les étiquettes des émotions détectées
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertit l'image capturée en nuances de gris
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray)  # Détecte les visages dans l'image

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Dessine un rectangle autour de chaque visage détecté
            roi_gray = gray[y:y + h, x:x + w]  # Extrait la région d'intérêt (ROI) du visage
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)  # Redimensionne l'ROI pour le modèle

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0  # Normalise l'ROI
                roi = img_to_array(roi)  # Convertit l'ROI en tableau numpy
                roi = np.expand_dims(roi, axis=0)  # Ajoute une dimension pour correspondre à l'entrée du modèle

                prediction = classifier.predict(roi)[0]  # Prédit l'émotion du visage
                label = emotion_labels[prediction.argmax()]  # Obtient le libellé de l'émotion avec la probabilité la plus élevée
                label_position = (x, y)
                cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Affiche l'émotion sur l'image

        # Affiche le flux vidéo et les étiquettes des émotions dans Streamlit
        st.image(frame, channels="BGR", use_column_width=True)
        st.write(f"Emotion Detected: {label}")
    else:
        st.error("Failed to read from webcam.")  # Affiche une erreur si l'image ne peut pas être lue

    if st.button("Stop"):
        cap.release()  # Libère la capture vidéo
        cv2.destroyAllWindows()  

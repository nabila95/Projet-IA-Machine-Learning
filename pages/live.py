import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

# Charger le modèle de détection d'émotion
classifier = load_model('C:/Users/Muthuvel/OneDrive - Ecole IPSSI/M2/Intelligence artificielle - Machine learning/Projet/model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

st.title("Emotion Detection App")

# Initialiser la variable de label
label = "No Faces"  # Valeur par défaut

# Créer un bouton dans l'application pour démarrer/arrêter le flux vidéo
run = st.checkbox('Run')

# Initialiser la fenêtre d'affichage du flux vidéo
FRAME_WINDOW = st.image([])

# Ouvrir la webcam
camera = cv2.VideoCapture(0)

while run:
    ret, frame = camera.read()
    if ret:
        # Convertir l'image de BGR à RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convertir l'image capturée en nuances de gris pour la détection des visages
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            # Dessiner un rectangle autour de chaque visage détecté
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Préparer le ROI pour la prédiction d'émotion
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # Prédire l'émotion du visage
                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]
                label_position = (x, y - 10)
                cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # Afficher le flux vidéo avec les émotions détectées
        FRAME_WINDOW.image(frame)

    else:
        st.error("Failed to read from webcam.")

    # Ajouter un bouton pour arrêter le flux vidéo
    if st.button("Stop"):
        run = False

if not run:
    camera.release()  # Libérer la capture vidéo
    cv2.destroyAllWindows()
    st.write('Stopped')

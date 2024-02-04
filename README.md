# Projet de Détection d'Émotion

## Description
Ce projet est une application de détection d'émotion qui utilise un modèle de réseau de neurones convolutionnels (CNN) construit avec Keras, une API de réseaux de neurones de haut niveau écrite en Python et capable de s'exécuter sur TensorFlow. L'application analyse les images fournies par l'utilisateur et détecte les émotions affichées par les personnes sur les photos, avec un niveau de précision indiqué.

[User] --(Upload Image/Interact)--> [Streamlit UI]
  |
  |---[Image Upload]--> [Server/Backend] --(Image Processing)--> [OpenCV & Numpy]
  |       |
  |       |---(Processed Image)--> [Machine Learning Model with Keras]
  |                   |
  |                   |---(Analysis/Results)--> [Data Visualization in Tableau]
  |
  |---[View Tableau Dashboard]--> [Embedded Tableau in Streamlit UI]



## Modèle CNN
Le modèle CNN a été entraîné pour reconnaître diverses émotions en utilisant un large ensemble de données d'images faciales. Le modèle identifie les émotions suivantes : colère, dégoût, peur, bonheur, neutralité, tristesse et surprise.

![image](https://github.com/Muthuvel15/Projet-IA-Machine-Learning/assets/60102777/5e82c06f-ab2a-46d4-8ca4-bed60f0a8748)



## Utilisation d'OpenCV
OpenCV est utilisé pour le traitement d'image préalable, y compris la conversion des images en niveaux de gris et la détection des visages avant de les passer au modèle de classification des émotions.

## Fonctionnalités Supplémentaires
L'application offre également la possibilité de détecter les émotions en temps réel via une webcam, en utilisant le même modèle de CNN.



#### Projet de Détection des Émotions

Ce projet utilise un modèle CNN (réseau de neurones convolutifs) conçu avec Keras et utilise OpenCV pour le traitement d'images en temps réel.

## Exemples de Prédiction

### Happy emotion avec 95.8% accuracy

<img src="./image/capture_ecran/happy.png" width="300" alt="Happy Emotion" title="Happy Emotion">

### Sad emotion avec 46.54% accuracy

<img src="./image/capture_ecran/sad.png" width="300" alt="sad Emotion" title="sad Emotion">

### Surprise emotion avec 94.22% accuracy

<img src="./image/capture_ecran/surprise.png" width="300" alt="surprise Emotion" title="surprise Emotion">


## Installation
Pour exécuter l'application, vous aurez besoin des bibliothèques suivantes :
- Keras
- OpenCV
- Numpy
- Streamlit (pour l'interface utilisateur web)

## Fichier de Requis (requirements.txt)
```
numpy==1.xx.x
opencv-python-headless==4.xx.x
streamlit==1.xx.x
keras==2.xx.x
tensorflow==2.xx.x
Pillow==8.xx.x
```
*Remarque : Remplacez "xx" par les numéros de version les plus récents et compatibles.*

## Exécution
Pour lancer l'application, utilisez la commande suivante :
```sh
streamlit run home.py
```

## Contribution
SAVOUNDIRAPANDIANE Muthuvel / Nabila EL ABDALI / Jihene BEN AMEUR / Claudia TIMOCI



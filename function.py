import base64
from selenium.webdriver import Chrome
import requests, random, time
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import *
from io import BytesIO
import pandas as pd


# Fonction pour convertir les données en CSV pour le téléchargement
def to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue().decode('utf-8')

# Fonction pour créer un lien de téléchargement
def create_download_link(csv_content, filename):
    b64 = base64.b64encode(csv_content.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger le fichier CSV</a>'
    return href


def fetch_data():
    # Create a connection to your database
    database = DataBase('pokemon')
    # Fetch data from the database, convert it to a pandas DataFrame
    # Modify the query as per your database structure
    query = "SELECT * FROM poke"
    df = pd.read_sql(query, database.connection)

    return df

#  
def scraping_pokemon_cards(n_cards=10):
    # Connexion à la base de données
    database = DataBase('pokemon')

    # Création d'une table
    database.create_table('poke',
        national=db.Integer,
        name=db.String,
        types=db.String,
        image=db.String,
        link=db.String,
        Species=db.String,
        height=db.String,
        weight=db.String,
    )

    # Instancier le navigateur Chrome
    driver = Chrome()

    # Ouvrir l'URL contenant les cartes Pokémon
    driver.get("https://pokemondb.net/pokedex/national")

    # Attendre que la page se charge complètement
    time.sleep(2)  # Attendre un peu plus longtemps pour assurer le chargement complet

    # Rechercher les cartes Pokémon
    cards = driver.find_elements(By.CLASS_NAME, "infocard")

    # Parcourir chaque carte Pokémon pour collecter les informations
    for card in range(1, n_cards):
        try:
            # Extraire les détails de la carte
            name = cards[card].find_element(By.CLASS_NAME, "ent-name").text
            types = cards[card].find_element(By.CLASS_NAME, "type-icon").text


            image = cards[card].find_element(By.TAG_NAME, "img").get_attribute("src")
            link = cards[card].find_element(By.TAG_NAME, "a").get_attribute("href")

            # Récupérer les informations détaillées de la carte
            driver.get(link)
            time.sleep(1)

            national = driver.find_element(By.TAG_NAME, 'strong').text
            details_section = driver.find_element(By.TAG_NAME, 'tbody')
            Species = details_section.find_elements(By.TAG_NAME, 'tr')[2].find_element(By.TAG_NAME, 'td').text
            height = details_section.find_elements(By.TAG_NAME, 'tr')[3].find_element(By.TAG_NAME, 'td').text
            weight = details_section.find_elements(By.TAG_NAME, 'tr')[4].find_element(By.TAG_NAME, 'td').text

            driver.back()
            time.sleep(1)

            # Ajouter les informations à la base de données
            database.add_row('poke',
                national=national,
                name=name,
                types=types,
                image=image,
                link=link,
                Species=Species,
                height=height,
                weight=weight,
            )
        except Exception as e:
            print(f"Erreur lors de la collecte des données pour la carte {card}: {e}")

    driver.quit()
    return "Collecte des cartes Pokémon terminée et enregistrement dans la base de données."






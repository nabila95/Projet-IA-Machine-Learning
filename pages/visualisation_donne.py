import streamlit as st
import pandas as pd
from database import DataBase

def fetch_data():
    database = DataBase('pokemon')
    query = "SELECT * FROM poke"
    df = pd.read_sql(query, database.connection)
    return df

def main():
    st.title("Visualisation des Collectes Pokémon")

    df = fetch_data()

    for index, row in df.iterrows():
        # Use a container to enclose each Pokémon's data
        with st.container():
            cols = st.columns(2)
            with cols[0]:
                st.image(row['image'], width=150)
            with cols[1]:
                st.markdown(f"**Name**: {row['name']}")
                st.markdown(f"**Species**: {row['species']}")
                st.markdown(f"**Height**: {row['height']}")
                st.markdown(f"**Weight**: {row['weight']}")
                st.markdown(f"**Type**: {row['types']}")

            # Optional: Add a horizontal line for separation
            st.markdown("---")

if __name__ == "__main__":
    main()

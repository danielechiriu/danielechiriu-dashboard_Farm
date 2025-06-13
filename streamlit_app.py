import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Allevamento", layout="wide")
st.title("📊 Dashboard Allevamento")

# Link al file Drive (pubblico, leggibile)
file_id = "1Vc65p1geR74D2Vg9VjDaxtHoo29M6z6U"
url = f"https://drive.google.com/uc?id={file_id}&export=download"

try:
    # Caricamento del file
    df = pd.read_csv(url, sep=";", header=None)
    df.columns = ["Operatore", "Timestamp", "Allevatore", "Specie", "Codice", "DataEvento",
                  "Categoria", "Azione", "Note", "Latitudine", "Longitudine"]
    
    # Filtro per operatore
    operatore = st.text_input("Filtra per operatore (es: Ricci, Chiriu, Pinna)")
    if operatore:
        df = df[df["Operatore"].str.lower() == operatore.lower()]

    st.dataframe(df)

    # Mostra mappa se ci sono coordinate valide
    if not df.empty and "Latitudine" in df.columns and "Longitudine" in df.columns:
        with st.expander("📍 Mappa"):
            st.map(df[["Latitudine", "Longitudine"]])

except Exception as e:
    st.error(f"Errore nel caricamento del file: {e}")

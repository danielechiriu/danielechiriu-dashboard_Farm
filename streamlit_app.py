import streamlit as st
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import StringIO
import os

# Usa il tuo file client_secret
SECRET_FILE = "/Users/danielechiriu/Dropbox/APP IOS/client_secret_263743908793-lfpjkf5o9rc12r776l25en7465p1jkbl.apps.googleusercontent.com.json"
FOLDER_ID = "15D4CvmmWF9mTAHIMynvAb2CTQnpou5nR"

@st.cache_resource
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(SECRET_FILE)
    gauth.LocalWebserverAuth()  # Si aprirà una finestra del browser al primo avvio
    return GoogleDrive(gauth)

@st.cache_data
def load_data(drive):
    file_list = drive.ListFile({'q': f"'{FOLDER_ID}' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == 'Data_Farm.txt':
            content = file.GetContentString()
            df = pd.read_csv(StringIO(content), sep=';')
            return df
    st.error("❌ File 'Data_Farm.txt' non trovato nella cartella.")
    return pd.DataFrame()

st.title("📊 Dashboard da Google Drive - Data_Farm.txt")

drive = authenticate_drive()
df = load_data(drive)
df.columns = ["Operatore", "Timestamp", "Allevatore", "Specie", "Codice", "DataEvento", "Categoria", "Azione", "Note", "Latitudine", "Longitudine"]

st.dataframe(df)

if not df.empty:
    st.subheader("Anteprima dei dati:")
    st.dataframe(df)
    st.subheader("Statistiche:")
    st.write(df.describe())
else:
    st.warning("⚠️ Nessun dato disponibile.")

import streamlit as st
import pandas as pd
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

st.set_page_config(page_title="Dashboard Allevamento", layout="wide")
st.title("📊 Dashboard Allevamento")

# Carica credenziali
creds = service_account.Credentials.from_service_account_file(
    "service_account.json",  # Assicurati che il file esista nel repo
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

# Crea servizio Drive
drive_service = build("drive", "v3", credentials=creds)

# ID del file Drive (devi sostituire con il tuo reale)
file_id = "1aBcDefGhIjKlMnOpQrStUvWxYz"

# Scarica il file
request = drive_service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)

done = False
while not done:
    status, done = downloader.next_chunk()

# Leggi il contenuto
fh.seek(0)
df = pd.read_csv(fh, sep=";", header=None)
df.columns = ["Operatore", "Timestamp", "Allevatore", "Specie", "Codice", "DataEvento", "Categoria", "Azione", "Note", "Latitudine", "Longitudine"]

# Filtro per operatore se passato nell'URL
operatore_param = st.query_params.get("operatore", None)
if operatore_param:
    df = df[df["Operatore"].str.strip().str.lower() == operatore_param.lower()]
    st.subheader(f"Dati per l'operatore: {operatore_param}")

# Mostra dati
st.dataframe(df)

# Mappa (se lat/long sono validi)
if not df.empty:
    with st.expander("📍 Mappa interventi"):
        st.map(df[["Latitudine", "Longitudine"]])

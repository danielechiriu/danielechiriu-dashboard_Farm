from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st
import pandas as pd
import io

# Carica credenziali
creds = service_account.Credentials.from_service_account_file(
    "service_account.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

drive_service = build("drive", "v3", credentials=creds)

# ID del file Dati_Farm.txt
file_id = "1aBcDefGhIjKlMnOpQrStUvWxYz"

# Scarica contenuto
request = drive_service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()

fh.seek(0)
df = pd.read_csv(fh, sep=";", header=None)
df.columns = ["Operatore", "Timestamp", "Allevatore", "Specie", "Codice", "DataEvento", "Categoria", "Azione", "Note", "Latitudine", "Longitudine"]
st.dataframe(df)


# app.py (Main Entry Point)
import threading
import time
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import folium
from streamlit_folium import st_folium
from flask import Flask, request, jsonify
from streamlit_autorefresh import st_autorefresh
from cryptography.fernet import Fernet
import base64
import json
import os

st.set_page_config(page_title="Examen 2 IoT", layout="wide")
st.title("🌡️ Examen 2: Internet de las Cosas: TEMA - End Devices")
app = Flask(__name__)
data_lock = threading.Lock()
data_path = "data.xlsx"


KEY = os.getenv("FERNET_KEY").encode()
cipher = Fernet(KEY)

# Initialize data
initial_data = pd.read_excel("./datainicial.xlsx")
#initial_data.to_excel(data_path, index=False)

# Función para descifrar datos
def decrypt_data(encrypted_text):
    try:
        decrypted_bytes = cipher.decrypt(base64.b64decode(encrypted_text))
        return json.loads(decrypted_bytes.decode('utf-8'))
    except Exception as e:
        print("Error al descifrar:", e)
        return None

@app.route("/data", methods=["POST"])
def update_data():
    global data_path
    try:
        encrypted_payload = request.get_json().get("data")
        new_data = decrypt_data(encrypted_payload)
        
        if not new_data:
            return jsonify({"error": "Datos no válidos"}), 400

        print(new_data["CODIGO"])
        print(new_data["LONGITUD"])
        print(new_data["LATITUD"])
        print(new_data["TEMPERATURA"])
        
        dfcambiar = pd.read_excel(data_path)
        dfcambiar.loc[dfcambiar["CODIGO"] == int(new_data["CODIGO"]), ["LATITUD", "LONGITUD", "TEMPERATURA"]] = [
            new_data["LATITUD"], new_data["LONGITUD"], new_data["TEMPERATURA"]
        ]
        dfcambiar.to_excel(data_path, index=False)
        return jsonify({"message": "Datos actualizados correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# Llave generada ZohCE66Y1IpT6OQzfQpt_OHbv-pPEqzws-xdJcEXxOo=
#from cryptography.fernet import Fernet

#key = Fernet.generate_key()
#print(key.decode())  # Copia la clave generada
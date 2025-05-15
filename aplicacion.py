import streamlit as st
import numpy as np
from PIL import Image
import base64
from datetime import datetime
import openpyxl
from openpyxl import Workbook
from tensorflow.keras.models import load_model
import pandas as pd  # Asegúrate de tener pandas instalado
import io  # Necesario para BytesIO
import gdown
import streamlit.components.v1 as components

# Lista de clases (etiquetas) de tu modelo
class_names = [
    'TANGARA DE LENTEJUELAS', 'TANGARA MATORRALERA', 'TANGARA NUQUIRRUFA', 'TANGARA PINTOJA', 'PINTOJA PALMERA',
    'TANGARA AZULGRIS', 'TANGARA AZULINEGRA', 'TANGARA CABECIAZUL', 'TANGARA CAPUCHA DORADA', 'TANGARA CORONINEGRA',
    'CHIPE AMARILLO FINAL', 'CHIPE CABEZA NEGRA FINAL', 'CHIPE CASTAÑO FINAL', 'CHIPE DORSO VERDE FINAL',
    'CHIPE FLANCOS CASTAÑOS FINAL', 'CHIPE GARGANTA AMARILLA FINAL', 'CHIPE GARGANTA NARANJA FINAL',
    'CHIPE GORRA CANELA SUREÑO FINAL', 'TROPICAL PARULA FINAL'
]

# Descripciones de las clases
class_descriptions = {
    'TANGARA DE LENTEJUELAS': "La tangara de lentejuelas se caracteriza por su vibrante coloración verde y azul...",
    'TANGARA MATORRALERA': "Esta especie habita los matorrales y tiene un plumaje colorido...",
    # Agrega el resto de las descripciones aquí
}

# Cargar modelo entrenado
file_id = "1rh2AvU4O0aboTqIN_BLh_u1D5J868Aln"
url = f"https://drive.google.com/uc?id={file_id}"
model_path = "best_model.keras"
gdown.download(url, model_path, quiet=False)

# Cargar el modelo
model = load_model(model_path)
print("✅ Modelo cargado correctamente desde Google Drive")

# Función para guardar avistamientos en el Excel
def guardar_avistamiento(lat, lng, prediction):
    archivo = "avistamientos.xlsx"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        wb = openpyxl.load_workbook(archivo)
        sheet = wb.active
    except FileNotFoundError:
        wb = Workbook()
        sheet = wb.active
        sheet.append(["Latitud", "Longitud", "Predicción", "Fecha y Hora"])
    sheet.append([lat, lng, prediction, now])
    wb.save(archivo)

# Obtener los avistamientos registrados desde el archivo Excel
def obtener_avistamientos():
    archivo = "avistamientos.xlsx"
    avistamientos = []
    try:
        wb = openpyxl.load_workbook(archivo)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            avistamientos.append({
                'lat': row[0],
                'lng': row[1],
                'prediction': row[2],
                'fecha_hora': row[3]
            })
    except FileNotFoundError:
        print(f"Error: El archivo {archivo} no fue encontrado.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    return avistamientos

# Streamlit UI
st.title('Clasificador de Aves')

# Subir archivo de imagen
uploaded_file = st.file_uploader("Sube una imagen de un ave", type=["jpg", "jpeg", "png"])

prediction = None
description = None
image_data = None

# Clasificación de imagen
if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB').resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    preds = model.predict(img_array)
    idx = np.argmax(preds, axis=1)[0]
    prediction = class_names[idx]
    description = class_descriptions.get(prediction, "Descripción no disponible.")
    
    # Mostrar imagen clasificada
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    st.image(img, caption="Imagen clasificada", use_column_width=True)
    st.subheader(f"Predicción: {prediction}")
    st.write(description)

# Inputs para registrar avistamientos
lat = st.number_input('Latitud', format="%.6f")
lng = st.number_input('Longitud', format="%.6f")

if st.button('Guardar Avistamiento'):
    if lat and lng:
        guardar_avistamiento(lat, lng, prediction)
        st.success('Avistamiento guardado exitosamente!')
    else:
        st.error('Por favor, ingrese una latitud y longitud válidas.')

# Mostrar avistamientos registrados
st.subheader('Avistamientos Registrados')
avistamientos = obtener_avistamientos()

# Mostrar los avistamientos en una tabla
if avistamientos:
    df_avistamientos = pd.DataFrame(avistamientos)
    st.write(df_avistamientos)

    # Mostrar en el mapa (Google Maps o Streamlit map)
    st.map(df_avistamientos[['lat', 'lng']])  # Mostrar en el mapa
else:
    st.write("No se han registrado avistamientos.")

# Incluir el mapa de Google Maps con la API
st.subheader('Ubicación de los Avistamientos')

# Incluyendo Google Maps con API Key
google_maps_html = """
<div style="width: 100%; height: 500px;">
    <iframe width="100%" height="100%" 
        src="https://www.google.com/maps/embed/v1/place?key=AIzaSyCZR_MdAc09QAW0nWJvlCdcwIx_CQQoM2Y
            &q=Latitud,Lng" frameborder="0" style="border:0;" allowfullscreen>
    </iframe>
</div>
"""
# Reemplazamos las coordenadas de los avistamientos en el mapa de Google
if avistamientos:
    last_avistamiento = avistamientos[-1]  # Tomamos el último avistamiento
    google_maps_html = google_maps_html.replace("Latitud", str(last_avistamiento['lat']))
    google_maps_html = google_maps_html.replace("Lng", str(last_avistamiento['lng']))
    components.html(google_maps_html, height=500)


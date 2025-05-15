import streamlit as st
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Lista de clases (etiquetas) de tu modelo
class_names = [
    'TANGARA DE LENTEJUELAS', 'TANGARA MATORRALERA', 'TANGARA NUQUIRRUFA', 'TANGARA PINTOJA', 'PINTOJA PALMERA',
    'TANGARA AZULGRIS', 'TANGARA AZULINEGRA', 'TANGARA CABECIAZUL', 'TANGARA CAPUCHA DORADA', 'TANGARA CORONINEGRA',
    'CHIPE AMARILLO FINAL', 'CHIPE CABEZA NEGRA FINAL', 'CHIPE CASTAÑO FINAL', 'CHIPE DORSO VERDE FINAL', 'CHIPE FLANCOS CASTAÑOS FINAL',
    'CHIPE GARGANTA AMARILLA FINAL', 'CHIPE GARGANTA NARANJA FINAL', 'CHIPE GORRA CANELA SUREÑO FINAL', 'TROPICAL PARULA FINAL'
]

# Diccionario con las descripciones de las clases
class_descriptions = {
    'TANGARA DE LENTEJUELAS': "La tangara de lentejuelas se caracteriza por su vibrante coloración verde y azul, con reflejos metálicos que imitan lentejuelas.",
    'TANGARA MATORRALERA': "Esta especie habita los matorrales y tiene un plumaje colorido que va desde el verde hasta el rojo y amarillo.",
    'TANGARA NUQUIRRUFA': "Una tangara de tonos predominantes en verde y amarillos, conocida por su canto melodioso.",
    'TANGARA PINTOJA': "La tangara pintoja es una especie que destaca por su colorido plumaje en tonos marrones y anaranjados.",
    'PINTOJA PALMERA': "Esta especie habita las palmas de América Central, y su plumaje presenta una mezcla de tonos marrones y verdes.",
    'TANGARA AZULGRIS': "Con su distintivo color azul grisáceo, esta tangara se encuentra en las selvas tropicales de Sudamérica.",
    'TANGARA AZULINEGRA': "Una especie con colores que van desde el azul eléctrico hasta el negro, visible en zonas de montaña.",
    'TANGARA CABECIAZUL': "La tangara cabeciazul tiene una característica coloración azul en su cabeza y pecho, con el resto de su cuerpo en tonos verdes.",
    'TANGARA CAPUCHA DORADA': "Con su característica capucha dorada, esta tangara es un espectáculo visual en las selvas tropicales.",
    'TANGARA CORONINEGRA': "Su característica es su corona negra y plumaje colorido en tonos rojos y amarillos.",
    'CHIPE AMARILLO FINAL': "Un pequeño chip de color amarillo brillante que habita áreas abiertas y bordes de bosque.",
    'CHIPE CABEZA NEGRA FINAL': "Este chip tiene una cabeza negra contrastante con el resto de su cuerpo de colores más apagados.",
    'CHIPE CASTAÑO FINAL': "Un chip de color castaño, con una excelente capacidad para camuflarse en su hábitat natural.",
    'CHIPE DORSO VERDE FINAL': "Con un característico dorso verde, este chip es común en áreas boscosas.",
    'CHIPE FLANCOS CASTAÑOS FINAL': "Este chip tiene flancos castaños y una notable capacidad para moverse rápidamente entre los arbustos.",
    'CHIPE GARGANTA AMARILLA FINAL': "Con una garganta de color amarillo brillante, este chip es fácil de identificar entre la vegetación.",
    'CHIPE GARGANTA NARANJA FINAL': "Similar al anterior, pero con una garganta de color naranja intenso.",
    'CHIPE GORRA CANELA SUREÑO FINAL': "Este chip se destaca por su gorra de color canela, especialmente visible en los climas sureños.",
    'TROPICAL PARULA FINAL': "Un pequeño y vibrante pájaro de los trópicos, conocido por sus colores brillantes y su comportamiento activo."
}

# Cargar tu modelo personalizado (asegúrate de tener el archivo .h5 en el directorio adecuado)
model = load_model('models/model_VGG16_v.keras')

# Título de la aplicación
st.title("Clasificador de Imágenes con Keras")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostrar la imagen cargada
    img = Image.open(uploaded_file)

    # Convertir la imagen a RGB (en caso de que sea RGBA)
    img = img.convert('RGB')

    st.image(img, caption="Imagen cargada", use_column_width=True)

    # Preprocesar la imagen para el modelo
    img = img.resize((224, 224))  # Tamaño esperado por muchos modelos (ajusta según tu modelo)
    img_array = np.array(img)
    
    # Convertir la imagen a formato compatible con Keras
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalización si es necesario (dependiendo del entrenamiento)

    # Realizar la predicción
    predictions = model.predict(img_array)

    # Obtener la clase predicha (índice)
    predicted_class_idx = np.argmax(predictions, axis=1)[0]

    # Obtener el nombre de la clase predicha usando el índice
    predicted_class_name = class_names[predicted_class_idx]

    # Obtener la descripción de la clase predicha
    predicted_class_description = class_descriptions.get(predicted_class_name, "No hay descripción disponible.")

    # Mostrar los resultados
    st.subheader("Predicción:")
    st.write(f"La clase predicha es: **{predicted_class_name}** con probabilidad de {np.max(predictions) * 100:.2f}%")
    st.subheader("Descripción:")
    st.write(predicted_class_description)

import cv2
import torch
import numpy as np
from ultralytics import YOLO
import os

# Cargar el modelo YOLO
modelo = YOLO('yolov8n.pt')  # Puedes cambiar a otro modelo si lo prefieres

def procesar_imagenes_recursivo(carpeta_entrada, carpeta_salida):
    for raiz, carpetas, archivos in os.walk(carpeta_entrada):
        for archivo in archivos:
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                ruta_entrada = os.path.join(raiz, archivo)

                # Crear la estructura de carpetas en la salida
                ruta_relativa = os.path.relpath(raiz, carpeta_entrada)
                carpeta_destino = os.path.join(carpeta_salida, ruta_relativa)
                os.makedirs(carpeta_destino, exist_ok=True)

                # Leer la imagen
                imagen = cv2.imread(ruta_entrada)

                if imagen is not None:
                    # Detectar objetos con YOLO
                    resultados = modelo(imagen)

                    for resultado in resultados:
                        cajas = resultado.boxes.xyxy.cpu().numpy()
                        clases = resultado.boxes.cls.cpu().numpy()
                        for caja, clase in zip(cajas, clases):
                            if clase == 14:  # Clase 14 es 'pájaro' en YOLO
                                x1, y1, x2, y2 = map(int, caja)
                                # Recortar la imagen alrededor del pájaro
                                pajaro_recortado = imagen[y1:y2, x1:x2]
                                # Redimensionar a 224x224
                                pajaro_redimensionado = cv2.resize(pajaro_recortado, (224, 224))
                                # Guardar la imagen en la carpeta correspondiente
                                ruta_salida = os.path.join(carpeta_destino, archivo)
                                cv2.imwrite(ruta_salida, pajaro_redimensionado)
                                break

# Rutas de entrada y salida
carpeta_entrada = 'C:\\Users\\Fabian\\Desktop\\Traspaso de imagenes\\Imagenes'
carpeta_salida = 'C:\\Users\\Fabian\\Desktop\\Traspaso de imagenes\\Imagenes\\Aves preprocesado'

# Ejecutar el procesamiento recursivo
procesar_imagenes_recursivo(carpeta_entrada, carpeta_salida)

print("✅ Procesamiento completado.")
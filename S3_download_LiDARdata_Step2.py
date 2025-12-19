import requests
import time
import os
import sys

"""
This script is used to automatically download LiDAR .laz files.
STEP 1: S2_download_LiDARdata_Step1.py (previous script)
STEP 2: S3_download_LiDARdata_Step2.py (this script)

This script takes the .txt file generated in STEP 1.
This file contains the URLs of the ‘.laz’ files to be downloaded and automatically downloads them to the disk,
waiting for an interval between downloads.
It automatically creates a folder (CARPETA_DESTINO), where we have to indicate where we want to save it and the name.
"""

# ================================================
# CONFIGURATION
# ================================================

# IMPORTANT: Change the path of the file generated in STEP 1 (ARCHIVO_URLS) if necessary.
ARCHIVO_URLS = r"C:\PhD\LiDAR\Datos\Enlaces_descarga_archivos.txt"

# IMPORTANT: Set the path to the destination folder you create to save the downloaded .laz files. YOU DO NOT NEED TO CREATE IT IN ADVANCE.
CARPETA_DESTINO = r"C:\PhD\LiDAR\Datos\Descargados\Originales"

# Time interval between discharges (in minutes)
INTERVALO_MINUTOS = 1

# ================================================
# SCRIPT
# ================================================

def leer_urls(archivo):
    """
    Lee el archivo de texto y devuelve una lista de URLs.
    """
    if not os.path.exists(archivo):
        print(f"ERROR: No se encontró el archivo '{archivo}'")
        sys.exit(1)

    with open(archivo, "r", encoding="utf-8") as f:
        urls = [linea.strip() for linea in f if linea.strip()]

    if not urls:
        print("El archivo no contiene URLs.")
        sys.exit(1)

    return urls

def obtener_nombre_unico(ruta_base):
    """
    Dado un path base, devuelve uno único añadiendo sufijo numérico si existe.
    Ejemplo: si "file.laz" existe, intenta "file_1.laz", "file_2.laz", etc.
    """
    base, ext = os.path.splitext(ruta_base)
    contador = 1
    ruta_nueva = ruta_base
    while os.path.exists(ruta_nueva):
        ruta_nueva = f"{base}_{contador}{ext}"
        contador += 1
    return ruta_nueva

# Función para descargar los archivos .laz
def descargar_todas_las_urls(urls, intervalo_minutos, carpeta_destino):
    """
    Descarga todos los archivos de la lista de URLs con un intervalo entre descargas.
    Renombra los archivos descargados conservando solo los últimos 20 caracteres del nombre.
    """
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    total = len(urls)
    print(f"Se descargarán {total} archivos, con un intervalo de {intervalo_minutos} minuto(s) entre descargas.\n")

    for i, url in enumerate(urls, 1):
        nombre_original = url.split("/")[-1]
        ruta_temporal = os.path.join(carpeta_destino, nombre_original)

        print(f"[{i}/{total}] Descargando: {url}")

        resp = requests.get(url, stream=True)

        if resp.status_code == 200:
            with open(ruta_temporal, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Renombrar usando los últimos 20 caracteres del nombre original
            nuevo_nombre = nombre_original[-20:]
            ruta_renombrada = os.path.join(carpeta_destino, nuevo_nombre)
            ruta_renombrada = obtener_nombre_unico(ruta_renombrada)
            os.rename(ruta_temporal, ruta_renombrada)

            print(f"Archivo guardado como: {ruta_renombrada}\n")
        else:
            print(f"ERROR al descargar {url}. Código de estado: {resp.status_code}\n")

        if i < total:
            print(f"Esperando {intervalo_minutos} minuto(s)...\n")
            time.sleep(intervalo_minutos * 60)  # Tiempo de espera en segundos

    print("Todas las descargas han finalizado.")

# ================================================

if __name__ == "__main__":
    urls = leer_urls(ARCHIVO_URLS)
    descargar_todas_las_urls(urls, INTERVALO_MINUTOS, CARPETA_DESTINO)

# If you CTRL+click on the link that appears below on the VisualStudio Code ‘OUTPUT’ screen,
# follow the link and it will take you to the web page, so you can see how long it will take to download completely.
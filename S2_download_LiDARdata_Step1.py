import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys

"""
This script is used to automatically download LiDAR .laz files.
STEP 1: S2_download_LiDARdata_Step1.py (this script)
STEP 2: S3_download_LiDARdata_Step2.py (next script to be used)
"""

# ============================================
# === CONFIGURATION ============
# ============================================

# IMPORTANT: Modify the web link where the data is located (BASE_URL).
BASE_URL = "https://datacloud.icgc.cat/datacloud/lidar-territorial/laz_unzip/"
print("Reading the base URL...")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

# IMPORTANT: Adjust the location of the input .txt file containing the names of the .laz files you wish to download (NOMBRES_ARCHIVO).
NOMBRES_ARCHIVO = r"C:/PhD/LiDAR/LaTordera/archivos_descargar_v3_LaTordera.txt"
print("Leyendo archivo .txt con los nombres de los archivos a descargar...")

# IMPORTANT: Adjust the output file name (ARCHIVO_SALIDA) where the download links for these files will be saved.
ARCHIVO_SALIDA = r"C:/PhD/LiDAR/LaTordera/Enlaces_descarga_archivos.txt"


# ============================================
# === SCRIPT ==================
# ============================================

# Read the names of the files collected in the input .txt file
def leer_nombres_archivo(NOMBRES_ARCHIVO):
    """
    Devuelve un conjunto con los nombres de los archivos a descargar.
    """
    if not os.path.exists(NOMBRES_ARCHIVO):
        print(f"Error: No se encontró el archivo {NOMBRES_ARCHIVO}")
        sys.exit(1)

    with open(NOMBRES_ARCHIVO, "r", encoding="utf-8") as f:
        nombres = {line.strip() for line in f if line.strip()}

    print(f"{len(nombres)} nombres de archivo leídos.")
    return nombres

# Obtain the list of subdirectories from the main page
def obtener_directorios(BASE_URL):
    """
    Devuelve una lista de URLs de directorios en la URL base.
    """
    print(f"Accediendo a {BASE_URL}...")
    resp = requests.get(BASE_URL, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Error al acceder a {BASE_URL}. Código: {resp.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    directorios = [a["href"] for a in soup.find_all("a") if a["href"].endswith("/")]
    print(f"{len(directorios)} directorios encontrados.")
    return directorios

# Search for links ending in ‘/’ (subdirectories)
def obtener_archivos(url_directorio):
    """
    Devuelve una lista de nombres de archivos en un directorio dado.
    """
    print(f"Explorando: {url_directorio}")
    resp = requests.get(url_directorio, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Error al acceder a {url_directorio}. Código: {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    archivos = [a["href"] for a in soup.find_all("a") if not a["href"].endswith("/")]
    return archivos


# ============================================

def main():
    nombres_objetivo = leer_nombres_archivo(NOMBRES_ARCHIVO)
    directorios = obtener_directorios(BASE_URL)

    encontrados = 0

# Open the output file to write the URLs
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f_output:
        for dir_href in directorios:
            url_dir = urljoin(BASE_URL, dir_href)
            archivos = obtener_archivos(url_dir)

            for archivo_href in archivos:
                nombre_archivo = archivo_href.split("/")[-1]
                if nombre_archivo in nombres_objetivo:
                    url_completo = urljoin(url_dir, archivo_href)
                    f_output.write(url_completo + "\n")
                    encontrados += 1
                    print(f"Encontrado: {nombre_archivo}")

    print(f"Proceso finalizado. {encontrados} URLs guardadas en '{ARCHIVO_SALIDA}'.")


# ============================================

if __name__ == "__main__":
    main()

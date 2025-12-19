# Script to add ‘.laz’ to the end of each line in a .txt file
# Overwrites the original file

archivo = 'C:/PhD/LiDAR/Datos/archivos_descargar_v3_LaTordera.txt'  # Cambia este nombre si tu archivo se llama diferente

# Read all lines
with open(archivo, 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Add ‘.laz’ to each line (avoid duplicating if you already have it)
lineas_modificadas = []
for linea in lineas:
    linea = linea.strip()
    if not linea.endswith('.laz'):
        linea += '.laz'
    lineas_modificadas.append(linea + '\n')

# Overwrite the original file
with open(archivo, 'w', encoding='utf-8') as f:
    f.writelines(lineas_modificadas)

print(f'Se añadieron ".laz" a las líneas de {archivo}')

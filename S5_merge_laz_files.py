import os
import subprocess
import glob

# IMPORTANT: modify these paths according to your system
carpeta_laz = r"C:/PhD/LiDAR/Datos-laz/Converted_copia/merged3/merged2/merged1"
lasmerge_path = r"C:/lastools/bin/lasmerge64.exe"

# Create a subfolder called ‘merged’ inside the input folder (where the .laz files to be merged are located).
carpeta_salida = os.path.join(carpeta_laz, "merged")
os.makedirs(carpeta_salida, exist_ok=True)

# Get all .laz files
archivos = glob.glob(os.path.join(carpeta_laz, "*.laz"))
archivos.sort()  # Sort by name, optional

# Group files in sets of 7; they will be joined in sets of 7, which is what the unlicensed version allows.
grupos = [archivos[i:i + 7] for i in range(0, len(archivos), 7)]

for idx, grupo in enumerate(grupos, 1):
    nombre_base = f"merged_{idx:03d}"
    salida_archivo = os.path.join(carpeta_salida, f"{nombre_base}.laz")
    log_txt = os.path.join(carpeta_salida, f"{nombre_base}.txt")
    
    # Build "lasmerge" command
    comando = [lasmerge_path]
    for archivo in grupo:
        comando.extend(["-i", archivo])
    comando.extend(["-o", salida_archivo])
    
    # Display on console
    print(f"Fusionando grupo {idx}:")
    for archivo in grupo:
        print(f"  - {archivo}")
    print(f"  => Guardado como: {salida_archivo}\n")
    
    # Run the command
    try:
        subprocess.run(comando, check=True)
        
        # Save log file with list of merged files
        with open(log_txt, "w") as f:
            f.write(f"Archivos fusionados en {nombre_base}.laz:\n")
            for archivo in grupo:
                f.write(f"{os.path.basename(archivo)}\n")
                
    except subprocess.CalledProcessError as e:
        print(f"Error al procesar el grupo {idx}: {e}")

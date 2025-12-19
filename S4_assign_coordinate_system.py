import os
import subprocess

# IMPORTANT: Modify these paths according to your system.
LASTOOLS_PATH = r"C:/LAStools/bin/las2las64.exe"  # Tool for assigning SRS to a .laz file
INPUT_FOLDER = r"C:/PhD/LiDAR/Datos-laz/V2_2016-17_ICGC"  # Folder containing .laz files
OUTPUT_FOLDER = r"C:/PhD/LiDAR/Datos-laz/Converted"  # Folder for storing files with assigned coordinate system
EPSG_CODE = 25831  # EPSG code to assign (ETRS89 / UTM zone 31N). IMPORTANT: CHANGE IF NECESSARY.

# Verificar si la carpeta de salida existe, si no, crearla
if not os.path.exists(OUTPUT_FOLDER):
    print(f"Creando carpeta de salida: {OUTPUT_FOLDER}")
    os.makedirs(OUTPUT_FOLDER)

# Get list of .laz files
laz_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.laz')]
laz_files = laz_files[:500]  # Limitar a 500 archivos si hay más

if not laz_files:
    print("No se encontraron archivos .laz en la carpeta indicada.")
    exit(1)

# Create list of full paths to files
input_paths = [os.path.join(INPUT_FOLDER, f) for f in laz_files]

# Verify the coordinate system for each file and assign one if necessary.
def check_and_assign_srs(file_path, output_path):
    # Command to obtain information about the coordinate system of the .laz file
    command_info = [LASTOOLS_PATH, "-i", file_path]
    
    try:
        # Run the las2las command to verify the coordinate system
        result = subprocess.run(command_info, capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "Projection" in line:
                print(f"Sistema de coordenadas para {file_path}: {line.strip()}")
                return True  # The file already has a coordinate system.
        # If you do not have a coordinate system, assign one.
        print(f"No se encontró sistema de coordenadas para {file_path}, asignando EPSG:{EPSG_CODE}...")
        # Assign EPSG coordinate system
        command_assign_srs = [
            LASTOOLS_PATH, "-i", file_path, "-o", output_path, "-epsg", str(EPSG_CODE)
        ]
        subprocess.run(command_assign_srs, check=True)
        print(f"Sistema de coordenadas asignado a {file_path} y guardado en {output_path}")
        return False  # A new coordinate system was assigned.
    except subprocess.CalledProcessError as e:
        print(f"Error al procesar {file_path}: {e}")
        return False

# Process the files
for i, file in enumerate(input_paths):
    print(f"\nProcesando archivo {i + 1}/{len(input_paths)}: {file}")
    output_file = os.path.join(OUTPUT_FOLDER, os.path.basename(file))  # Output file

    # Verify and assign SRS if necessary
    check_and_assign_srs(file, output_file)

print("\nProceso completado.")

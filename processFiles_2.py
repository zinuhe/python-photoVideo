# python renamer.py "Boda" -d --dry-run


import os
import sys
import argparse
import datetime
from pathlib import Path
# pip install icecream (Opcional, se puede usar print normal)
try:
    from icecream import ic
except ImportError:
    ic = print  # Fallback si no está instalado

# Constantes
# Usamos un set para búsqueda rápida y normalizamos a minúsculas para evitar duplicados
PHOTO_EXTENSIONS = {'.dng', '.jpeg', '.jpg', '.jpe', '.png'}
VIDEO_EXTENSIONS = {'.mov', '.mp4'}

def get_valid_files(extensions):
    """Obtiene archivos del directorio actual que coincidan con las extensiones."""
    current_dir = Path('.')
    # Iteramos sobre todos los archivos y filtramos por sufijo (case insensitive)
    files = [
        f for f in current_dir.iterdir() 
        if f.is_file() and f.suffix.lower() in extensions
    ]
    return files

def get_creation_time(file_path):
    """
    Intenta obtener la fecha de creación de forma compatible con varios OS.
    Si falla, usa la fecha de modificación.
    """
    stat = file_path.stat()
    try:
        # st_birthtime funciona en Mac/Windows
        return stat.st_birthtime
    except AttributeError:
        # Fallback para Linux (usa última modificación)
        return stat.st_mtime

def sort_files(files, by_date=False):
    """Ordena los archivos por nombre o por fecha de creación/modificación."""
    if by_date:
        # Ordena por timestamp de creación
        return sorted(files, key=lambda f: get_creation_time(f))
    else:
        # Ordena alfabéticamente
        return sorted(files, key=lambda f: f.name)

def generate_new_name(file_path, event_name, index, total_files, use_date_prefix):
    """Genera el nuevo nombre del archivo basado en la lógica deseada."""
    
    # Calcular ceros a la izquierda dinámicamente (ej: 100 archivos -> 3 dígitos)
    padding = len(str(total_files))
    if padding < 2: padding = 2
    
    sequence_str = f"{index:0{padding}d}"
    original_stem = file_path.stem
    extension = file_path.suffix

    # Lógica para preservar prefijos del nombre original (basado en tu código anterior)
    # Si hay un guion bajo, mantenemos lo que está antes. Si no, usamos el evento.
    prefix = ""
    if event_name:
        if "_" in original_stem:
            prefix = original_stem.split('_')[0] + "_" + event_name + "_"
        else:
            prefix = event_name + "_"
    else:
        # Si no hay evento, intentamos mantener la estructura original
        if "_" in original_stem:
            # Encuentra el último guion bajo y toma todo lo anterior
            prefix = original_stem.rsplit('_', 1)[0] + "_"
        else:
            prefix = original_stem + "_"

    date_part = ""
    if use_date_prefix:
        ts = get_creation_time(file_path)
        dt = datetime.datetime.fromtimestamp(ts)
        date_part = dt.strftime('%Y-%m-%d') + "-"

    new_name = f"{date_part}{prefix}{sequence_str}{extension}"
    return file_path.with_name(new_name)

def process_renaming(files, event_name, use_date_prefix, dry_run=False):
    """Ejecuta el renombrado."""
    renamed_count = 0
    total = len(files)

    print(f"--- Procesando {total} archivos ---")
    
    for i, file_path in enumerate(files, start=1):
        new_file_path = generate_new_name(file_path, event_name, i, total, use_date_prefix)
        
        if new_file_path == file_path:
            continue

        if new_file_path.exists():
            print(f"[ALERTA] El archivo ya existe, saltando: {new_file_path.name}")
            continue

        try:
            if not dry_run:
                file_path.rename(new_file_path)
                ic(f"Renombrado: {file_path.name} -> {new_file_path.name}")
            else:
                print(f"[Simulacro] {file_path.name} -> {new_file_path.name}")
            renamed_count += 1
        except OSError as e:
            print(f"[ERROR] No se pudo renombrar {file_path.name}: {e}")

    print(f"--- Finalizado. Archivos renombrados: {renamed_count} ---")

def main():
    # Configuración de argumentos robusta
    parser = argparse.ArgumentParser(description="Renombrador masivo de fotos y videos.")
    parser.add_argument("event", nargs="?", default="", help="Nombre del evento para insertar en el archivo")
    parser.add_argument("-d", "--date-sort", action="store_true", help="Ordenar archivos por fecha antes de renombrar")
    parser.add_argument("-f", "--folder-name", action="store_true", help="Usar el nombre de la carpeta actual como nombre del evento")
    parser.add_argument("-rbd", "--rename-by-date", action="store_true", help="Agregar la fecha de creación al inicio del nombre")
    parser.add_argument("--dry-run", action="store_true", help="Solo muestra qué pasaría, no renombra nada realmente")

    args = parser.parse_args()

    # Lógica del nombre del evento
    event_name = args.event
    if args.folder_name:
        event_name = Path.cwd().name
    
    # Recolectar archivos (Fotos y Videos combinados)
    # Nota: Puedes separar las listas si quieres secuencias independientes (ej: foto_01, video_01)
    # Aquí los junto para una secuencia única (archivo_01, archivo_02...)
    all_extensions = PHOTO_EXTENSIONS.union(VIDEO_EXTENSIONS)
    files = get_valid_files(all_extensions)

    if not files:
        print("No se encontraron archivos válidos en este directorio.")
        return

    # Ordenar
    sorted_files = sort_files(files, by_date=args.date_sort)

    # Renombrar
    process_renaming(sorted_files, event_name, args.rename_by_date, args.dry_run)

if __name__ == "__main__":
    main()

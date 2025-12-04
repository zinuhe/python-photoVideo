# Para solo ajustar la fecha de la carpeta:
# python processFoldersDates.py

# Para ajustar la fecha Y renombrar la carpeta (agregar mes/día):
# python processFoldersDates.py --rename

# Modo Simulacro (Seguro) Verás qué pasaría, pero la carpeta quedará intacta.
# python processFoldersDates.py --rename --dry-run


import os
import datetime
import argparse
import platform
import subprocess
from pathlib import Path

# Intentar importar icecream, si no, usar print
try:
    from icecream import ic
except ImportError:
    ic = print

# Extensiones válidas (case insensitive en la lógica de búsqueda)
EXTENSIONS = {'.dng', '.jpeg', '.jpg', '.jpe', '.png', '.mov', '.mp4'}

def get_valid_files(folder_path):
    """Retorna una lista de archivos válidos en el path dado."""
    return [
        f for f in folder_path.iterdir() 
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    ]

def get_file_timestamp(file_path):
    """
    Obtiene el timestamp más antiguo disponible (Creación o Modificación).
    """
    stat = file_path.stat()
    try:
        # st_birthtime es creación (Mac/Windows)
        return stat.st_birthtime
    except AttributeError:
        # st_mtime es modificación (Linux/Unix fallback)
        return stat.st_mtime

def get_oldest_timestamp(files):
    """Encuentra el timestamp más antiguo de una lista de archivos."""
    if not files:
        return None
    oldest_file = min(files, key=lambda f: get_file_timestamp(f))
    return get_file_timestamp(oldest_file)

def set_folder_date(folder_path, timestamp, dry_run=False):
    """
    Cambia la fecha de MODIFICACIÓN y ACCESO de la carpeta.
    Soporta Dry-Run.
    """
    dt_readable = datetime.datetime.fromtimestamp(timestamp)

    if dry_run:
        print(f"🔮 [DRY-RUN] Se cambiaría la fecha de '{folder_path.name}' a: {dt_readable}")
        # En dry-run también simulamos el aviso de MacOS si aplica
        if platform.system() == 'Darwin':
             print(f"🔮 [DRY-RUN] (MacOS) Se ejecutaría 'SetFile' para la fecha de creación.")
        return

    try:
        # os.utime espera (atime, mtime)
        os.utime(folder_path, (timestamp, timestamp))
        print(f"✅ Fecha modificada a: {dt_readable}")
        
        # HACK ESPECÍFICO PARA MACOS (Fecha de Creación)
        if platform.system() == 'Darwin':
            try:
                dt_str = dt_readable.strftime('%m/%d/%Y %H:%M:%S')
                subprocess.check_call(['SetFile', '-d', dt_str, str(folder_path)])
                print(f"🍎 (MacOS) Fecha de creación 'SetFile' aplicada.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

    except OSError as e:
        print(f"❌ Error al cambiar fecha de la carpeta: {e}")

def rename_folder_append_date(folder_path, timestamp, dry_run=False):
    """Renombra la carpeta agregando _MM_DD al final. Soporta Dry-Run."""
    dt = datetime.datetime.fromtimestamp(timestamp)
    suffix = dt.strftime('_%m_%d') # Ejemplo: _12_25
    
    # Evitar duplicar el sufijo
    if folder_path.name.endswith(suffix):
        print(f"⚠️ La carpeta ya tiene el sufijo {suffix}, no se renombra.")
        return folder_path

    new_name = folder_path.name + suffix
    new_path = folder_path.with_name(new_name)
    
    if dry_run:
        print(f"🔮 [DRY-RUN] Se renombraría la carpeta: '{folder_path.name}' -> '{new_name}'")
        # Retornamos el new_path simulado para que el resto del script muestre info coherente
        return new_path

    try:
        folder_path.rename(new_path)
        print(f"✅ Carpeta renombrada: '{folder_path.name}' -> '{new_path.name}'")
        return new_path
    except OSError as e:
        print(f"❌ Error al renombrar carpeta: {e}")
        return folder_path

def main():
    parser = argparse.ArgumentParser(description="Ajusta fecha de carpeta según archivo más antiguo.")
    parser.add_argument("--rename", action="store_true", help="Renombrar carpeta agregando _Mes_Dia")
    parser.add_argument("--path", type=str, default=".", help="Ruta de la carpeta a procesar (default: actual)")
    parser.add_argument("--dry-run", action="store_true", help="Simulacro: No realiza cambios reales")
    
    args = parser.parse_args()
    
    current_folder = Path(args.path).resolve()
    
    if args.dry_run:
        print("--- 🔮 MODO DRY-RUN (SIMULACRO) ACTIVO 🔮 ---")

    print(f"📂 Procesando carpeta: {current_folder}")

    files = get_valid_files(current_folder)
    
    if not files:
        print("⚠️ No se encontraron archivos de foto/video válidos en esta carpeta.")
        return

    # 1. Obtener la fecha más antigua
    oldest_ts = get_oldest_timestamp(files)
    ic(datetime.datetime.fromtimestamp(oldest_ts))

    # 2. Renombrar carpeta (Si se pide con --rename)
    if args.rename:
        # Pasamos el flag dry_run y recibimos la nueva ruta (real o simulada)
        current_folder = rename_folder_append_date(current_folder, oldest_ts, dry_run=args.dry_run)

    # 3. Actualizar fecha de la carpeta (en la ruta que corresponda)
    set_folder_date(current_folder, oldest_ts, dry_run=args.dry_run)

    if args.dry_run:
        print("--- 🏁 Fin del Simulacro ---")

if __name__ == "__main__":
    main()

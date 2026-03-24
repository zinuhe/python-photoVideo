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

# Extensiones válidas (case insensitive)
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
    # Prioriza birthtime (creación) si está disponible, si no usa mtime (modificación)
    return getattr(stat, 'st_birthtime', stat.st_mtime)

def get_oldest_timestamp(files):
    """Encuentra el timestamp más antiguo de una lista de archivos."""
    if not files:
        return None
    # Usamos min con una función clave para eficiencia
    return min(get_file_timestamp(f) for f in files)

def set_folder_date(folder_path, timestamp, dry_run=False):
    """
    Cambia la fecha de MODIFICACIÓN y ACCESO de la carpeta.
    Soporta MacOS (SetFile) para fecha de creación.
    """
    dt_readable = datetime.datetime.fromtimestamp(timestamp)

    if dry_run:
        print(f"🔮 [DRY-RUN] Se cambiaría fecha de '{folder_path.name}' a: {dt_readable}")
        if platform.system() == 'Darwin':
            print(f"🔮 [DRY-RUN] (MacOS) Se ejecutaría 'SetFile' para fecha de creación.")
        return

    try:
        # os.utime cambia acceso y modificación
        os.utime(folder_path, (timestamp, timestamp))
        print(f"✅ Fecha de modificación actualizada: {dt_readable.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # HACK ESPECÍFICO PARA MACOS (Fecha de Creación)
        if platform.system() == 'Darwin':
            try:
                # Formato requerido por SetFile: mm/dd/yyyy hh:mm:ss
                dt_str = dt_readable.strftime('%m/%d/%Y %H:%M:%S')
                subprocess.check_call(['SetFile', '-d', dt_str, str(folder_path)])
                print(f"🍎 (MacOS) Fecha de creación 'SetFile' aplicada.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ (MacOS) No se pudo aplicar SetFile. ¿Están instaladas las Command Line Tools?")

    except OSError as e:
        print(f"❌ Error al cambiar fecha de la carpeta: {e}")

def rename_folder_append_date(folder_path, timestamp, dry_run=False):
    """Renombra la carpeta agregando _MM_DD al final."""
    dt = datetime.datetime.fromtimestamp(timestamp)
    suffix = dt.strftime('_%m_%d') 
    
    # Evitar duplicar el sufijo o renombrar si ya termina así
    if folder_path.name.endswith(suffix):
        print(f"⚠️ La carpeta ya tiene el sufijo {suffix}, saltando renombrado.")
        return folder_path

    new_name = f"{folder_path.name}{suffix}"
    new_path = folder_path.with_name(new_name)
    
    if dry_run:
        print(f"🔮 [DRY-RUN] Renombrar: '{folder_path.name}' -> '{new_name}'")
        return new_path

    try:
        folder_path.rename(new_path)
        print(f"✅ Carpeta renombrada: '{new_name}'")
        return new_path
    except OSError as e:
        print(f"❌ Error al renombrar carpeta: {e}")
        return folder_path

def main():
    parser = argparse.ArgumentParser(description="Ajusta fecha de carpeta según archivo más antiguo.")
    parser.add_argument("--rename", action="store_true", help="Renombrar carpeta agregando _Mes_Dia")
    parser.add_argument("--path", type=str, default=".", help="Ruta de la carpeta (default: actual)")
    parser.add_argument("--dry-run", action="store_true", help="No realiza cambios reales")
    
    args = parser.parse_args()
    
    # Resolvemos la ruta absoluta para evitar ambigüedades
    target_folder = Path(args.path).resolve()
    
    if args.dry_run:
        print("\n" + "="*40)
        print("   🔮 MODO SIMULACRO ACTIVO 🔮")
        print("="*40 + "\n")

    if not target_folder.exists() or not target_folder.is_dir():
        print(f"❌ La ruta especificada no existe o no es una carpeta: {target_folder}")
        return

    print(f"📂 Carpeta objetivo: {target_folder}")

    files = get_valid_files(target_folder)
    
    if not files:
        print("⚠️ No se encontraron archivos multimedia válidos.")
        return

    # 1. Obtener la fecha más antigua de los archivos contenidos
    oldest_ts = get_oldest_timestamp(files)
    ic(datetime.datetime.fromtimestamp(oldest_ts))

    # 2. Renombrar (Opcional)
    # Guardamos la referencia de la carpeta (si cambia de nombre, la nueva ruta es necesaria para el paso 3)
    folder_to_touch = target_folder
    if args.rename:
        folder_to_touch = rename_folder_append_date(target_folder, oldest_ts, dry_run=args.dry_run)

    # 3. Actualizar los metadatos de tiempo de la carpeta
    set_folder_date(folder_to_touch, oldest_ts, dry_run=args.dry_run)

    if args.dry_run:
        print("\n--- 🏁 Fin del Simulacro ---")

if __name__ == "__main__":
    main()

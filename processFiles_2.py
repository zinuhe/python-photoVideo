# python renamer.py "Boda" -d --dry-run


import argparse
import datetime
from pathlib import Path

# --- CONSTANTES ---
PHOTO_EXTENSIONS = {'.dng', '.jpeg', '.jpg', '.jpe', '.png'}
VIDEO_EXTENSIONS = {'.mov', '.mp4'}
ALL_EXTS = PHOTO_EXTENSIONS | VIDEO_EXTENSIONS

def get_creation_time(file_path):
    stat = file_path.stat()
    # Priorizamos birthtime, si no mtime
    return getattr(stat, 'st_birthtime', stat.st_mtime)

def generate_new_name(file_path, event_name, index, total_files, use_date_prefix):
    padding = max(2, len(str(total_files)))
    sequence = f"{index:0{padding}d}"
    
    # Lógica de prefijos simplificada
    original_stem = file_path.stem
    if "_" in original_stem:
        base_prefix = original_stem.split('_')[0]
    else:
        base_prefix = original_stem

    final_prefix = f"{base_prefix}_{event_name}" if event_name else base_prefix
    
    date_str = ""
    if use_date_prefix:
        dt = datetime.datetime.fromtimestamp(get_creation_time(file_path))
        date_str = f"{dt.strftime('%Y-%m-%d')}-"

    return f"{date_str}{final_prefix}_{sequence}{file_path.suffix}"

def process_renaming(files, event_name, use_date_prefix, dry_run=False):
    total = len(files)
    renamed = 0

    for i, old_path in enumerate(files, 1):
        new_name = generate_new_name(old_path, event_name, i, total, use_date_prefix)
        new_path = old_path.with_name(new_name)

        if old_path == new_path:
            continue

        # Evitar sobrescribir archivos existentes
        if new_path.exists() and not dry_run:
            print(f"⚠️ Saltando: {new_name} ya existe.")
            continue

        action = "[DRY-RUN]" if dry_run else "[OK]"
        print(f"{action} {old_path.name} -> {new_name}")

        if not dry_run:
            try:
                old_path.rename(new_path)
                renamed += 1
            except Exception as e:
                print(f"❌ Error en {old_path.name}: {e}")

    print(f"\n✨ Proceso completado. Modificados: {renamed}/{total}")

def main():
    parser = argparse.ArgumentParser(description="Renombrador Pro")
    parser.add_argument("event", nargs="?", default="")
    parser.add_argument("-d", "--date-sort", action="store_true")
    parser.add_argument("-f", "--folder-name", action="store_true")
    parser.add_argument("-rbd", "--rename-by-date", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    event = Path.cwd().name if args.folder_name else args.event
    
    # Obtener y ordenar en un solo paso usando una expresión generadora
    files = [f for f in Path('.').iterdir() if f.is_file() and f.suffix.lower() in ALL_EXTS]
    
    if args.date_sort:
        files.sort(key=get_creation_time)
    else:
        files.sort(key=lambda x: x.name.lower())

    if not files:
        print("No hay archivos que procesar.")
        return

    process_renaming(files, event, args.rename_by_date, args.dry_run)

if __name__ == "__main__":
    main()

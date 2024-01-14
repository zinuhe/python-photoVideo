# To execute and DELETE
# The original file is in 
# /Users/jimmysaavedra/Documents/DEV/Python/SourceCode/Watchdog/changeCopy.py
# Cambios directos en processPhotoVideoSony.py este script 
#copia y ejecuta el script en el otro folder

# Python3 changeCopy.py

import time
import os, shutil, glob
import os.path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# File to watch
fileToWatch = "processPhotoVideoSony.py" #"*.py" #"*"

# Destination path
DEST_FILE = "/Users/jimmysaavedra/Documents/DEV/Python/DCIM_Jun-24/processPhotoVideoSony.py"

if __name__ == "__main__":
    patterns = [fileToWatch]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


def on_modified(event):
    now = datetime.now()
    now = now.strftime("%d/%b/%Y %H:%M:%S")
    copyFile(event.src_path, DEST_FILE)
    print(f"Copying... {now}")
    print(f"Src: {event.src_path}")
    print(f"Dst: {DEST_FILE} \n")
    # exec(open(DEST_FILE).read())  #EXEC

def on_moved(event):
    print(f"-- {event.src_path} was moved to {event.dest_path}")


def copyFile(source, destination, symlinks=False, ignore=None):    
    shutil.copy(source, destination)

my_event_handler.on_modified = on_modified

path = "."
go_recursively = False
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()

# Python3 processPhotoVideoSony.py
# To process folders and files (photos) from Sony camera, 
# it will set the folder and file names according to 'created date'
# ASSUMING dates on folders and files are correct

# TODO
# -linea 60 de donde saca esa fecha? Porque no usa la fecha de EXIF (parece que ya quedo, probar mas)
# -DONE--linea 59 si son mas de 999 falla, por el i:03 leer primero cuantos files hay en el folder
# -DONE--esta leyendo todos los archivos solo deberia leer photo files, add PHOTO_TYPES
# -DONE---a la segunda vez, si algun archivo fue removido no funciona bien, pierde el conteo
# -preguntar por parametro si usar "_event_" o algo diferente

import os, shutil, glob, sys
import exifread #pip3 install exifread
import os.path, time, calendar
from subprocess import check_output, check_call
from datetime import datetime
 
# Photo files extensions allowed
PHOTO_TYPES = ['.DNG', '.JPE', '.JPEG', '.JPG', '.PNG']

# Current working directory
currentPath = os.getcwd() + "/"

# Only Folders
folders = next(os.walk(currentPath))[1] # for the current dir use ('.')
folders.sort()
#print(folders)

for folder in folders:
    # Get files inside folder and sort them out
    files = os.listdir(currentPath + "/" + folder)
    files.sort()

    # Get number of files and set secuence
    _secuence = "03"
    if len(files) > 999: _secuence = "04"

    # Stores smallest date from files inside folder
    # to rename the folder with that date
    smallestDatetime = datetime(2100, 12, 31)

    # for i, file in enumerate(files, start=1):
    i = 1
    for file in files:
        # get file extension
        fileExtension = os.path.splitext(file)[1]
        # print(f"fileExtension: {fileExtension}")
        
        # Filter only PHOTO_TYPES files
        if fileExtension.upper() in PHOTO_TYPES:
            # Open image file for reading (binary mode)
            f = open(currentPath + folder + "/" + file, 'rb')

            # Return Exif tags
            tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeDigitized')

            if bool(tags):
                # YYYY:MM:DD H:M:S
                dateFromExif = tags['EXIF DateTimeDigitized']
                # print(f"dateFromExif: {dateFromExif}")

                # convert to datetime - 2021-07-09 09:42:07
                dateTimeFromExif = datetime.strptime(str(dateFromExif), '%Y:%m:%d %H:%M:%S')
                #print(f"{dateTimeFromExif.year}-{dateTimeFromExif.month}-{dateTimeFromExif.day}"")

                # smallestDatetime, store and compare
                # print(f"Type dateFromExif: {type(dateFromExif)}")
                # print(f"Type dateTimeFromExif: {type(dateTimeFromExif)}")
                if dateTimeFromExif < smallestDatetime:
                    smallestDatetime = dateTimeFromExif

                # YYYY-MM-DD_event_001.ext
                ## newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
                newFileName = dateTimeFromExif.strftime('%Y-%m-%d') + "_event_" + f"{i:{_secuence}}"
                #print(f"newFileName: {newFileName}")

                newFileName = newFileName + fileExtension
                #print(f"newFileName: {newFileName}")

                if file != newFileName:
                    # Renaming files
                    try:
                        os.rename(folder + "/" + file, folder + "/" + newFileName)
                        #print(f"Renaming file: {folder}/{file} --> {folder}/{newFileName}")
                    except OSError:
                        print(f"Renaming file operation failed: {folder}/{file} --> {folder}/{newFileName}")
                        sys.exit()
                i += 1
            else:
                print(f"No EXIF data for: '{folder}/{file}' file was not renamed")
        else:
            print(f"Not a photo file '{folder}/{file}'")


    #print(f"smallestDatetime: {smallestDatetime}")

    newFolderName = smallestDatetime.strftime("event_%b-%d") #get month name from datetime object
    # print(f"newFolderName: {newFolderName}")

    if newFolderName != '':
        if newFolderName != folder:
            try:
                # Rename folder
                #print(f"Renaming folder: {folder} --> {newFolderName}")
                os.rename(folder, newFolderName)
            except OSError:
                print(f"Renaming folder operation failed: {folder} --> {newFolderName}")
                sys.exit()
    else:
        print(f"ERROR - Getting new folder name for {folder} fails - probably date is not valid")


    #print("\n\n")


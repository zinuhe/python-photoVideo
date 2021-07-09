# Python3 processPhotoVideoSony.py
# To process folders and files (photos) from Sony camera, 
# it will set the folder and file names according to 'created date'
# ASSUMING dates on folders and files are correct

# TODO
# -linea 60 de donde saca esa fecha? Porque no usa la fecha de EXIF

import os, shutil, glob, sys
import exifread #pip3 install exifread
import os.path, time, calendar
from subprocess import check_output, check_call
from datetime import datetime
 
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

    # Stores smallest date from files inside folder
    # to rename the folder with that date
    smallestDatetime = datetime(2100, 12, 31)

    for i, file in enumerate(files, start=1):
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
            # print(f"dateTimeFromExif: {dateTimeFromExif}")

            #print(f"{dateTimeFromExif.year}-{dateTimeFromExif.month}-{dateTimeFromExif.day}"")

            # smallestDatetime, store and compare
            # print(f"Type dateFromExif: {type(dateFromExif)}")
            # print(f"Type dateTimeFromExif: {type(dateTimeFromExif)}")

            if dateTimeFromExif < smallestDatetime:
                smallestDatetime = dateTimeFromExif


            # YYYY-MM-DD_event_001.ext
            ## newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
            newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder + "/" + file))) + f'{i:03}'
            
            tmp = time.localtime(os.path.getmtime(currentPath + folder + "/" + file))
            print(f"time.localtime(os.path.getmtime(currentPath + folder + / + file)): {tmp}")
            #newFileName = time.strftime('%Y-%m-%d_event_', dateFromExif) + f'{i:03}'
            #print(f"newFileName: {newFileName}")

            fileExtension = os.path.splitext(file)[1]
            #print(f"fileExtension: {fileExtension}")

            newFileName = newFileName + fileExtension
            # print(f"newFileName: {newFileName}")


            if file != newFileName:
                # Renaming files
                try:
                    # os.rename(folder + "/" + file, folder + "/" + newFileName)
                    print(f"Renaming file: {folder}/{file} --> {folder}/{newFileName}")
                except OSError:
                    print(f"Renaming file operation failed: {folder}/{file} --> {folder}/{newFileName}")
                    sys.exit()


    print(f"smallestDatetime: {smallestDatetime}")

    newFolderName = smallestDatetime.strftime("event_%b-%d") #get month name from datetime object
    # print(f"newFolderName: {newFolderName}")

    if newFolderName != '':
        if newFolderName != folder:
            try:
                # Rename folder
                print(f"Renaming folder: {folder} --> {newFolderName}")
                #os.rename(folder, newFolderName)
            except OSError:
                print(f"Renaming folder operation failed: {folder}/{file} --> {folder}/{newFileName}")
                sys.exit()
    else:
        print(f"ERROR - Getting new folder name for {folder} fails - probably date is not valid")


    print("\n\n")


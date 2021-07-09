# Python3 processPhotoVideoSony.py
# To process folders and files (photos) from Sony camera, 
# it will set the folder and file names according to 'created date'
# ASSUMING dates on folders and files are correct

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

            # convert string to date
            dateTimeFromFile = datetime.strptime(str(dateFromExif), '%Y:%m:%d %H:%M:%S')
            # 2021-02-03 09:42:07
            # print(f"dateTimeFromFile: {dateTimeFromFile}")

            #print(dateTimeFromFile.year)
            #print(dateTimeFromFile.month)
            #print(dateTimeFromFile.day)

            # smallestDatetime, store and compare
            # print(f"Type dateFromExif: {type(dateFromExif)}")
            # print(f"Type dateTimeFromFile: {type(dateTimeFromFile)}")
            # print (f"Type smallestDatetime: {type(smallestDatetime)}")
            # print ("\n")

            if dateTimeFromFile < smallestDatetime:
                smallestDatetime = dateTimeFromFile

            # get year
            strYear = str(dateFromExif)[0:4] #From EXIF info

            # get month
            strNumberMonth = str(dateFromExif)[5:7] #From EXIF info
            strNameMonth = calendar.month_abbr[int(strNumberMonth)]

            # get day
            strDay = str(dateFromExif)[8:10] #From EXIF info


            # YYYY-MM-DD_event_001.ext
            # newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
            newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder + "/" + file))) + f'{i:03}'
            #print(f"newFileName: {newFileName}")

            fileExtension = os.path.splitext(file)[1]
            #print(f"fileExtension: {fileExtension}")

            newFileName = newFileName + fileExtension
            print(f"newFileName: {newFileName}")


            if file != newFileName:
                # Rename files
                try:
                    # os.rename(folder + "/" + file, folder + "/" + newFileName)
                    print(f"renaming file {folder}/{file} --> {folder}/{newFileName}")
                except OSError:
                    print(f"Renaming file operation failed: {folder}/{file} --> {folder}/{newFileName}")
                    sys.exit()

                # printf(f"file: {folder}/{file}")
                # print("newFileName: " + folder + "/" + newFileName)

            print("\n")


    print(f"smallestDatetime: {smallestDatetime}")
    # smallestDate = str(smallestDatetime.date())
    # print(f"smallestDate: {smallestDate}")

    # newFolderName = time.strftime('event_%b-%d', time.localtime(os.path.getctime(currentPath + folder)))
    # dateTimeFromFile = datetime.strptime(str(dateFromExif), '%Y:%m:%d %H:%M:%S')
    # newFolderName = time.strftime('event_%b-%d', smallestDatetime) ***NO***
    # newFolderName = time.strftime('event_%b-%d', smallestDatetime)
    newFolderName = smallestDatetime.strftime("event_%b-%d") #get month name from datetime object


    print("newFolderName: " + newFolderName)
    # print("newFolderName: " + newFolderName)


    if newFolderName != '':
        if newFolderName != folder:
            try:
                # Rename folder
                print(f"Original folder name: {folder}")
                print(f"New folder name: {newFolderName}")
                #os.rename(folder, newFolderName)
            except OSError:
                print(f"Renaming folder operation failed: {folder}/{file} --> {folder}/{newFileName}")
                sys.exit()
    else:
        print(f"DATE {newFolderName} NOT VALID")


    print("\n\n")
# El problema es que la fecha de creacion del folder no es confiable, 
# funciona la primera vez pero despues no 
# porque trae la fecha de modificacion no la de creacion.

# TODO: entrar en cada folder recorrer todos los files y sacar la menor fecha de EXIF, DONE line 65
# luego modificar el nombre del folder con esa fecha y continuar


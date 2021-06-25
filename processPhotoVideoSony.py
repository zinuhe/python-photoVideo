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
    # Rename folder
    # newFolderName = time.strftime('event_%b-%d', time.localtime(os.path.getctime(currentPath + folder)))
    print("folder: " + folder)
    # print("newFolderName: " + newFolderName)
    
    # sys.exit()

    # Get files inside folder and sort them out
    files = os.listdir(currentPath + "/" + folder)
    files.sort()

    for i, file in enumerate(files, start=1):
        
        # Open image file for reading (binary mode)
        f = open(currentPath + folder + "/" + file, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeDigitized')

        if bool(tags):
            # YYYY:MM:DD H:M:S
            dateTimeDigitized = tags['EXIF DateTimeDigitized']
            print("dateTimeDigitized: " + str(dateTimeDigitized))

            ##ESTOY AQUI @@@@@@@@@@@@@@@@@@@

            datetime_obj = datetime.strptime(str(dateTimeDigitized), '%Y:%m:%d %H:%M:%S').date()
            # 2021-02-03 09:42:07
            print(datetime_obj)

            print(datetime_obj.year)
            print(datetime_obj.month)
            print(datetime_obj.day)

            # smallestDate 

            # get year
            strYear = str(dateTimeDigitized)[0:4]

            # get month
            strNumberMonth = str(dateTimeDigitized)[5:7]
            strNameMonth = calendar.month_abbr[int(strNumberMonth)]

            # get day
            strDay = str(dateTimeDigitized)[8:10]

            sys.exit()

        sys.exit()



        # YYYY-MM-DD_event_001.ext
        # newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
        newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder + "/" + file))) + f'{i:03}'
        
        fileExtension = os.path.splitext(file)[1]

        newFileName = newFileName + fileExtension

        if file != newFileName:
            # Rename files
            try:
                os.rename(folder + "/" + file, folder + "/" + newFileName)
            except OSError:
                print("Rename file operation fails for: " + folder + "/" + file + " --> " + folder + "/" + newFileName)
                sys.exit()
            
            # print("file: " + folder + "/" + file)
            # print("newFileName: " + folder + "/" + newFileName)



    if newFolderName != '':
        if newFolderName != folder:
            try:
                # Rename folder
                print("folder: " + folder)
                print("newFolderName: " + newFolderName)
                os.rename(folder, newFolderName)
            except OSError:
                print("Rename folder operation fails for: " + folder + "/" + file + " --> " + folder + "/" + newFileName)
                sys.exit()

    else:
        print("DATE %s NOT VALID" % newFolderName)


# El problema es que la fecha de creacion del folder no es confiable, funciona la primera vez pero despues no 
# porque trae es la fecha de modificacion no la de creacion.

# Lo que toca hacer es, entrar en la carpeta recorrer todos los files y sacar la menor fecha de EXIF, luego modificar el nombre 
# del folder con esa fecha y continuar



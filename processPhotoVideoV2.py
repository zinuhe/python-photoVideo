# Python3 ~/Documents/DEV/Python/SourceCode/PhotoVideo/processPhotoVideoV2.py
# To process photo and video files under same folder
# By example files from iPhone

# TODO
#El problema con los videos es que no los organiza por fecha hora, encuentra uno
#y lo mueve al directorio luego encuentra otro y lo numera 001 de nuevo pero ese
#ya existe en el directorio entoces falla
#1)Solucion odernarlos por fecha/hora antes de procesarlos y moverlos
#2)Verificar si en el folder ya hay un archivo y actualizar el indice antes de
#moverlo
#3)Mover primero todos los archivos a los respectivos folders y luego
#renombrarlos ordenadamente por hora
##NO ESTA FUNCIONANDO BIEN, cuando funciona no quedan bien ordenados

##EL PROBLEMA ES QUE CUANDO HACE EL SORT LO HACE POR NOMBRE EN LUGAR DE
## FECHA CREACION o MODIFICATION

##Solucion
#Crear un array con nombre, extension, fecha creacion EXIF, fecha creacion file
#Ordenar ese array por fecha creacion EXIF si no existe usar fecha creacion file


import os, shutil, glob
import exifread #pip install exifread
import os.path, time, calendar
from subprocess import check_output, check_call
from datetime import datetime

# Photo and Video files extensions allowed
PHOTO_TYPES = ('*.dng', '*.DNG', '*.jpe', '*.JPE', '*.jpeg', '*.JPEG', '*.jpg', '*.JPG', '*.png', '*.PNG')
VIDEO_TYPES = ('*.mov', '*.MOV', '*.mp4', '*.MP4')
EVENT_NAME = "_event_"


class file:
    def __init__(self, name, ext, exifCreation, exifModification, fileCreation, fileModification):
        self.name = name
        self.ext = ext
        self.exifCreation = exifCreation
        self.exifModification = exifModification
        self.fileCreation = fileCreation
        self.fileModification = fileModification


# Creates a new folder and return a boolean
def createFolder(pathNewFolder):
    isCreatedOrExists = False
    if os.path.isdir(pathNewFolder) == False:
        try:
            os.mkdir(pathNewFolder)
        except OSError:
            print(f"Creation of the directory {pathNewFolder} failed")
        else:
            # print(f"Successfully created the folder: {pathNewFolder}")
            isCreatedOrExists = True
    else:
        # print(f"Folder '{pathNewFolder}' already exists")
        isCreatedOrExists = True

    return isCreatedOrExists


# Gets file extensions and return an array of matching files sorted
def getNameFiles(p_extensionFiles):
    filesNames = []
    for ext in p_extensionFiles:
        filesNames.extend(glob.glob(ext))

    # filesNames.sort()
    # print(f"Files Names sort: {filesNames}")
    return filesNames


#WORKING HERE
def getFileInfo(listFilesNames):
    files = []

    for item in listFilesNames:
        # Open media file for reading (binary mode)
        f = open(currentPath + item, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeDigitized')

        try:
            if bool(tags):
                #print(f"tags['EXIF DateTimeOriginal']: {tags['EXIF DateTimeOriginal']}")
                dateFromExif = tags['EXIF DateTimeDigitized']
                # It needs to be converted to datetime - 2021-07-15 09:42:07
                dateFrom = datetime.strptime(str(dateFromExif), '%Y:%m:%d %H:%M:%S')
            else: #Not EXIF Info
                # get creation/modification date from the file
                # creationTime     = time.strftime('%Y-%m-%d', time.localtime(os.path.getctime(currentPath + file)))
                # modificationTime = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(currentPath + file)))
                dateFromCreationDate = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(currentPath + file)))
                dateFrom = datetime.strptime(str(dateFromCreationDate), '%Y-%m-%d')
        except OSError:
            print(f"Path {currentPath} does not exist or is inaccessible")
            sys.exit()

        # appending instances to list files
        files.append(file(item, item, dateFrom, '', '', ''))

    print(f"FILES")
    x = sorted(files, key=lambda file:file.exifCreation)   # sort by exifCreation
    for f in x:
        print(f"{f.name}, {f.ext}, {f.exifCreation}, {f.exifModification}, {f.fileCreation}, {f.fileModification}")

    return files

# Iterates throught files and moves them
def processMediaFiles(mediaFiles, mediaPath):
    index = 1

    # for file in mediaFiles:
    for i, file in enumerate(mediaFiles, start=1):
        # Open media file for reading (binary mode)
        f = open(currentPath + file, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeDigitized')

        try:
            if bool(tags):
                #print(f"tags['EXIF DateTimeOriginal']: {tags['EXIF DateTimeOriginal']}")
                dateFromExif = tags['EXIF DateTimeDigitized']
                # It needs to be converted to datetime - 2021-07-15 09:42:07
                dateFrom = datetime.strptime(str(dateFromExif), '%Y:%m:%d %H:%M:%S')
            else: #Not EXIF Info
                # get creation/modification date from the file
                # creationTime     = time.strftime('%Y-%m-%d', time.localtime(os.path.getctime(currentPath + file)))
                # modificationTime = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(currentPath + file)))
                dateFromCreationDate = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(currentPath + file)))
                dateFrom = datetime.strptime(str(dateFromCreationDate), '%Y-%m-%d')
        except OSError:
            print(f"Path {currentPath} does not exist or is inaccessible")
            sys.exit()

        # get year
        strYear = str(dateFrom.year)

        # Creates subfolder with the year if it does't already exists
        createFolder(mediaPath + "/" + strYear)
        check_call(['Setfile', '-d', "01/01/" + strYear + " 01:00", mediaPath + "/" + strYear])

        # get month
        strNumberMonth = dateFrom.strftime('%m')
        strNameMonth = calendar.month_abbr[int(strNumberMonth)]

        # get day
        strDay = dateFrom.strftime('%d')


        if i == 1 :
            # Keep date to restart index
            keepDate = strYear + strNumberMonth + strDay
        elif keepDate == (strYear + strNumberMonth + strDay):
            index += 1
        else:
            index = 1
            keepDate = strYear + strNumberMonth + strDay

        newDate = "event_" + strNameMonth + "-" + strDay

        if newDate != '':
            if createFolder(mediaPath + "/" + strYear + "/" + newDate):
                # Set the proper date to the new folder just created
                tmpCreationDate =  strNumberMonth + "/" + strDay + "/" + strYear + " 01:00" #"12/20/2020 16:13"
                check_call(['Setfile', '-d', tmpCreationDate, mediaPath + "/" + strYear + "/" + newDate])

                fileExtension = os.path.splitext(file)[1]
                newFileName = strYear + "-" + strNumberMonth + "-" + strDay + EVENT_NAME + f'{index:03}' + fileExtension # {index:03} To add secuency
                os.rename(file, newFileName)
                # print(f"file: {file} | newFileName: {newFileName}")

                # Move the file (with new name) to the new folder
                shutil.move(newFileName, mediaPath + "/" + strYear + "/" + newDate)
                # time.sleep(0.5)
        else:
            print(f"DATE {newDate} NOT VALID")

    return

# Detects the current working directory
currentPath = os.getcwd() + "/"

# Prefix the name of the directory to be created
photoPath = currentPath + "photo"
videoPath = currentPath + "video"

# define the access rights
# access_rights = 0o755

photoFiles = getNameFiles(PHOTO_TYPES) #returns an array with photo files
videoFiles = getNameFiles(VIDEO_TYPES) #returns an array with video files

#NEW
photoFiles2 = getFileInfo(photoFiles) #returns an array with photo files

# if len(photoFiles) > 0:
#     createFolder(photoPath)
#     # Process photo files
#     processMediaFiles(photoFiles, photoPath)
#
# if len(videoFiles) > 0:
#     createFolder(videoPath)
#     # Process video files
#     processMediaFiles(videoFiles, videoPath)

# Python3 processPhotoVideo.py
# To process photo and video files under same folder
# By example files from iPhone

# TODO
# Checking dates from EXIF, it is better in processPhotoVideoSony
# With EXIF info and whitout it are similar, refactor it
# El problema con los videos puede ser por el orden a la hora
# de renombrar todo, primero ordernar por fecha y luego empezar a
# renombrar

import os, shutil, glob
import exifread #pip install exifread
import os.path, time, calendar
from subprocess import check_output, check_call
from datetime import datetime

# Photo and Video files extensions allowed
PHOTO_TYPES = ('*.dng', '*.DNG', '*.jpe', '*.JPE', '*.jpeg', '*.JPEG', '*.jpg', '*.JPG', '*.png', '*.PNG')
VIDEO_TYPES = ('*.mov', '*.MOV', '*.mp4', '*.MP4')
EVENT_NAME = "_event_"

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


# Gets file extensions and return an array of matching files
def getNameFiles(p_extensionFiles):
    filesNames = []
    for ext in p_extensionFiles:
        filesNames.extend(glob.glob(ext))

    # print(f"Files Names: {filesNames}")
    filesNames.sort()
    # print(f"Files Names sort: {filesNames}")
    return filesNames


# Iterates throught files and moves them
def processMediaFiles(mediaFiles, mediaPath):
    index = 1

    # for file in mediaFiles:
    for i, file in enumerate(mediaFiles, start=1):
        #print(f"file: {file}")

        # Open media file for reading (binary mode)
        f = open(currentPath + file, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeDigitized')

        if bool(tags):
            dateFromExif = tags['EXIF DateTimeDigitized']
            # print(f"dateFromExif: {dateFromExif}")

            # It needs to be converted to datetime - 2021-07-15 09:42:07
            dateTimeFromExif = datetime.strptime(str(dateFromExif), '%Y:%m:%d %H:%M:%S')
            # print(f"dateTimeFromExif: {dateTimeFromExif}")
            # print(f"{dateTimeFromExif.year}-{dateTimeFromExif.month}-{dateTimeFromExif.day}"")

            # get year
            strYear = str(dateTimeFromExif.year)

            # Creates subfolder with the year if it doesn't already exists
            createFolder(mediaPath + "/" + strYear)
            check_call(['Setfile', '-d', "01/01/" + strYear + " 01:00", mediaPath + "/" + strYear])

            # get month
            strNumberMonth = dateTimeFromExif.strftime('%m')
            strNameMonth = calendar.month_abbr[int(strNumberMonth)]

            # get day
            strDay = dateTimeFromExif.strftime('%d')

            if i == 1 :
                # Keep date to restart index
                keepDate = strYear + strNumberMonth + strDay
            elif keepDate == (strYear + strNumberMonth + strDay):
                index += 1
            else:
                index = 1
                keepDate = strYear + strNumberMonth + strDay

            dateTimeFromExif = "event_" + strNameMonth + "-" + strDay

            #print(f"dateTimeFromExif: {dateTimeFromExif}")

            if dateTimeFromExif != '':
                if createFolder(mediaPath + "/" + strYear + "/" + dateTimeFromExif):
                    # Set the proper date to the new folder just created
                    tmpCreationDate =  strNumberMonth + "/" + strDay + "/" + strYear + " 01:00" #"12/20/2020 16:13"
                    check_call(['Setfile', '-d', tmpCreationDate, mediaPath + "/" + strYear + "/" + dateTimeFromExif])

                    fileExtension = os.path.splitext(file)[1]
                    newFileName = strYear + "-" + strNumberMonth + "-" + strDay + EVENT_NAME + f'{index:03}' + fileExtension # {index:03} To add secuency
                    os.rename(file, newFileName)
                    # print(f"file: {file} | newFileName: {newFileName}")

                    # Move the file (with new name) to the new folder
                    shutil.move(newFileName, mediaPath + "/" + strYear + "/" + dateTimeFromExif)
            else:
                print(f"DATE {dateTimeFromExif} NOT VALID")
        else:
            print(f"Not EXIF Info for {currentPath}/{file}")

            try:
                # Create folder with creation/modification date from the file
                # modificationTime = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(currentPath + file)))
                # creationTime = time.strftime('%Y-%m-%d', time.localtime(os.path.getctime(currentPath + file)))

                # get year
                strYear = time.strftime('%Y', time.localtime(os.path.getmtime(currentPath + file)))

                # Creates subfolder with the year if it does't already exists
                createFolder(mediaPath + "/" + strYear)
                check_call(['Setfile', '-d', "01/01/" + strYear + " 01:00", mediaPath + "/" + strYear])

                # get month
                strNumberMonth = time.strftime('%m', time.localtime(os.path.getmtime(currentPath + file)))
                strNameMonth = calendar.month_abbr[int(strNumberMonth)]

                # get day
                strDay = time.strftime('%d', time.localtime(os.path.getmtime(currentPath + file)))

                if i == 1 :
                    # Keep date to restart index
                    keepDate = strYear + strNumberMonth + strDay
                elif keepDate == (strYear + strNumberMonth + strDay):
                    index += 1
                else:
                    index = 1
                    keepDate = strYear + strNumberMonth + strDay

                dateTimeFromExif = "event_" + strNameMonth + "-" + strDay

                #print(f"dateTimeFromExif: {dateTimeFromExif}")

                if dateTimeFromExif != '':
                    if createFolder(mediaPath + "/" + strYear + "/" + dateTimeFromExif):
                        # Set the proper date to the new folder just created
                        tmpCreationDate =  strNumberMonth + "/" + strDay + "/" + strYear + " 01:00" #"12/20/2020 16:13"
                        check_call(['Setfile', '-d', tmpCreationDate, mediaPath + "/" + strYear + "/" + dateTimeFromExif])

                        fileExtension = os.path.splitext(file)[1]
                        newFileName = strYear + "-" + strNumberMonth + "-" + strDay + EVENT_NAME + f'{index:03}' + fileExtension # {index:03} To add secuency
                        os.rename(file, newFileName)
                        # print(f"file: {file} | newFileName: {newFileName}")

                        # Move the file (with new name) to the new folder
                        shutil.move(newFileName, mediaPath + "/" + strYear + "/" + dateTimeFromExif)
                else:
                    print(f"DATE {dateTimeFromExif} NOT VALID")

            except OSError:
                print(f"Path {currentPath} does not exist or is inaccessible")
                sys.exit()

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

if len(photoFiles) > 0:
    createFolder(photoPath)
    # Process photo files
    processMediaFiles(photoFiles, photoPath)

if len(videoFiles) > 0:
    createFolder(videoPath)
    # Process video files
    processMediaFiles(videoFiles, videoPath)

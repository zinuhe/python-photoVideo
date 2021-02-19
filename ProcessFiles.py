#Python3 ProcessFiles.py
#To process photo and video files under only one folder
import os, shutil, glob
import exifread #pip install exifread
import os.path, time, calendar

from subprocess import check_output, check_call
#from datetime import datetime

PHOTO_TYPES = ('*.jpg', '*.JPG', '*.JPE', '*.jpe', '*.JPEG', '*.jpeg', '*.png', '*.PNG')
VIDEO_TYPES = ('*.mov', '*.MOV', '*.mp4', '*.MP4')

#Creates a new folder and return a boolean
def createFolder(pathNewFolder):
    isCreatedOrExists = False
    if os.path.isdir(pathNewFolder) == False:
        try:
            os.mkdir(pathNewFolder)
        except OSError:
            print ("Creation of the directory %s failed" % pathNewFolder)
        else:
            #print ("Successfully created the directory %s " % pathNewFolder)
            isCreatedOrExists = True
    else:
        #print ("Folder %s already exists " % pathNewFolder)
        isCreatedOrExists = True
    
    return isCreatedOrExists


#Gets extention files and return an array of matching files
def getNameFiles(p_extensionFiles):
    filesNames = []
    for ext in p_extensionFiles:
        filesNames.extend(glob.glob(ext))
    
    #print("Files Names: %s " % filesNames)
    filesNames.sort()
    #print("Files Names sort: %s " % filesNames)
    return filesNames


#Iterates throught files and moves them
def processMediaFiles(mediaFiles, mediaPath):
    index = 1

    #for file in mediaFiles:
    for i, file in enumerate(mediaFiles, start=1):
        #print("file: ", file)

        # Open image file for reading (binary mode)
        f = open(currentPath + file, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeDigitized')

        if bool(tags):
            dateTimeDigitized = tags['EXIF DateTimeDigitized']

            #validDateTimeDigitized = str(dateTimeDigitized)[0:10].replace(':', '-')

            #Convertir validDateTimeDigitized en formato fecha y usar linea 69 para sacar todo en una linea?

            #get year
            strYear = str(dateTimeDigitized)[0:4]

            #Creates subfolder with the year if it does't already exists
            createFolder(mediaPath + "/" + strYear)
            check_call(['Setfile', '-d', "01/01/" + strYear + " 01:00", mediaPath + "/" + strYear])

            #get month
            strNumberMonth = str(dateTimeDigitized)[5:7]
            strNameMonth = calendar.month_abbr[int(strNumberMonth)]

            #get day
            strDay = str(dateTimeDigitized)[8:10]

            if i == 1 :
                #Keep date to restart index
                keepDate = strYear + strNumberMonth + strDay
            elif keepDate == (strYear + strNumberMonth + strDay):
                index += 1
            else:
                index = 1
                keepDate = strYear + strNumberMonth + strDay

            validDateTimeDigitized = "event_" + strNameMonth + "-" + strDay
            #PROBAR ESTO validDateTimeDigitized = time.strftime('event_%b-%d', time.localtime(os.path.getmtime(currentPath + folder)))
            print(validDateTimeDigitized)

            if validDateTimeDigitized != '':
                if createFolder(mediaPath + "/" + strYear + "/" + validDateTimeDigitized):
                    #Set the propper date to the new folder just created
                    tmpCreationDate =  strNumberMonth + "/" + strDay + "/" + strYear + " 01:00" #"12/20/2020 16:13"
                    check_call(['Setfile', '-d', tmpCreationDate, mediaPath + "/" + strYear + "/" + validDateTimeDigitized])

                    #Rename files to format 2021-01-31_event_001.ext
                    #newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
                    newFileName = strYear + "-" + strNumberMonth + "-" + strDay + "_event_" + f'{index:03}' #To add secuency
                    os.rename(file, newFileName)
                    print("newFileName: %s" % newFileName)

                    #Move the file to the new folder
                    #shutil.move(file, mediaPath + "/" + strYear + "/" + validDateTimeDigitized) #WORKING
                    shutil.move(newFileName, mediaPath + "/" + strYear + "/" + validDateTimeDigitized)

                    #print("file: %s" % file)
            else:
                print("DATE %s NOT VALID" % validDateTimeDigitized)
        else:
            print("Not EXIF Info for %s" % currentPath + file)

            try:
                # Create folder with creation/modification date from the file
                #modificationTime = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(currentPath + file)))
                #creationTime = time.strftime('%Y-%m-%d', time.localtime(os.path.getctime(currentPath + file)))

                #get year
                strYear = time.strftime('%Y', time.localtime(os.path.getmtime(currentPath + file)))

                #Creates subfolder with the year if it does't already exists
                createFolder(mediaPath + "/" + strYear)
                check_call(['Setfile', '-d', "01/01/" + strYear + " 01:00", mediaPath + "/" + strYear])

                #get month
                strNumberMonth = time.strftime('%m', time.localtime(os.path.getmtime(currentPath + file)))
                strNameMonth = calendar.month_abbr[int(strNumberMonth)]

                #get day
                strDay = time.strftime('%d', time.localtime(os.path.getmtime(currentPath + file)))

                validDateTimeDigitized = "event_" + strNameMonth + "-" + strDay

                if validDateTimeDigitized != '':
                    if createFolder(mediaPath + "/" + strYear + "/" + validDateTimeDigitized):
                        #Set the proper date to the new folder just created
                        tmpCreationDate =  strNumberMonth + "/" + strDay + "/" + strYear + " 01:00" #"12/20/2020 16:13"
                        check_call(['Setfile', '-d', tmpCreationDate, mediaPath + "/" + strYear + "/" + validDateTimeDigitized])

                        #Move the file to the new folder
                        shutil.move(file, mediaPath + "/" + strYear + "/" + validDateTimeDigitized)
                else:
                    print("DATE %s NOT VALID" % validDateTimeDigitized)

                #print("Created: %s" % creationTime)
                #time.ctime(modification_time)
            except OSError:
                print("Path '%s' does not exists or is inaccessible" %currentPath)
                sys.exit

            # Move to (Photo/Video) root folder
            #shutil.move(file, mediaPath) #Igual mueve el archivo al folder del tipo de media
    return

# detect the current working directory
currentPath = os.getcwd() + "/"

# prefix the name of the directory to be created
photoPath = currentPath + "photo"
videoPath = currentPath + "video"

# define the access rights
#access_rights = 0o755

createFolder(photoPath)
createFolder(videoPath)

photoFiles = getNameFiles(PHOTO_TYPES) #return an array with photo files
videoFiles = getNameFiles(VIDEO_TYPES) #return an array with video files


#Process photo files
processMediaFiles(photoFiles, photoPath)

#Process video files
processMediaFiles(videoFiles, videoPath)



# Python3 ~/MyDocuments/Dev/python/python-photoVideo/processFoldersDates.py
# Python3 processFoldersDates.py

# To set up folder's creation date based on inside files creation dates

#TODO
#Go into a folder
#get files inside and get creation dates
#get the older file date
#set up the upper folder with that date
#Add '_month_day' at the end of folder's name?

import os, shutil, glob
import exifread #pip install exifread
import os.path, time, datetime, calendar
from subprocess import check_output, check_call
# from datetime import datetime
from icecream import ic #pip install icecream

# Photo and Video files extensions allowed
PHOTO_TYPES = ('*.dng', '*.DNG', '*.jpe', '*.JPE', '*.jpeg', '*.JPEG', '*.jpg', '*.JPG', '*.png', '*.PNG')
VIDEO_TYPES = ('*.mov', '*.MOV', '*.mp4', '*.MP4')
EVENT_NAME = "event_"
FOLDER_NAME = "FOLDER_NAME"

# To manage object file
class file:
    def __init__(self, name, year, monthNumber, monthName, day, fullDate, exifCreation):
        self.name = name
        self.year = year
        self.monthNumber = monthNumber
        self.monthName = monthName
        self.day = day
        self.fullDate = fullDate
        self.exifCreation = exifCreation


# Gets file extensions and return an array of matching files
def getNameFiles(p_extensionFiles):
    filesNames = []
    for ext in p_extensionFiles:
        filesNames.extend(glob.glob(ext))

    return filesNames

def getOldestDateFromFiles(listFilesNames):
    oldestDate = datetime.datetime.today()

    for fileName in listFilesNames:
        c_time = os.stat(currentPath + fileName).st_birthtime
        dt_c = datetime.datetime.fromtimestamp(c_time)
        if oldestDate > dt_c:
            oldestDate = dt_c

    return oldestDate


# Set the proper date to the new folder just created
# tmpCreationDate =  file.monthNumber + "/" + file.day + "/" + file.year + " 01:00" #"12/20/2020 16:13"
# check_call(['Setfile', '-d', tmpCreationDate, mediaPath + "/" + file.year + "/" + newDate])

# Gets the year from a given date
def getYear(inputDate):
    return str(inputDate.year)

# Gets the month from a given date
def getMonthNumber(inputDate):
    return inputDate.strftime('%m')

# Gets the month's name from a given date
def getMonthName(inputDate):
    return calendar.month_abbr[int(getMonthNumber(inputDate))]

# Gets the day from a given date
def getDay(inputDate):
    return inputDate.strftime('%d')

def getFullDate(inputDate):
    return getYear(inputDate) + getMonthNumber(inputDate) + getDay(inputDate)


# PROGRAM STARTS
# Gets the current working directory
currentPath = os.getcwd() + "/"

# Prefix the name of the directory to be created
photoPath = currentPath + "photo"
videoPath = currentPath + "video"

# define the access rights
# access_rights = 0o755

photoFiles = getNameFiles(PHOTO_TYPES) #returns an array with valid photo files
videoFiles = getNameFiles(VIDEO_TYPES) #returns an array with valid video files

# ic(photoFiles)

ic(getOldestDateFromFiles(photoFiles))

# Python3 ~/MyDocuments/DEV/Python/SourceCode/PhotoVideo/processFiles.py
# Python3 processFiles.py

# To re-name files after being processed
# It won't change dates, only numeration
# 2024-01-01_event_003.jpg
# 2024-01-01_event_005.jpg
# 2024-01-01_event_007.jpg
# To
# 2024-01-01_event_001.jpg
# 2024-01-01_event_002.jpg
# 2024-01-01_event_003.jpg

#TODO
# Read files from a folder, same folder, same date - [DONE]
# sort them by name - [DONE]
# Re-sequence them

import os, shutil, glob
import exifread #pip install exifread
import os.path, time, datetime, calendar
from subprocess import check_output, check_call
# from datetime import datetime
from icecream import ic #pip install icecream
from pathlib import Path

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

# def getOldestDateFromFiles(listFilesNames):
#     oldestDate = datetime.datetime.today()

#     for fileName in listFilesNames:
#         c_time = os.stat(currentPath + fileName).st_birthtime
#         dt_c = datetime.datetime.fromtimestamp(c_time)
#         if oldestDate > dt_c:
#             oldestDate = dt_c

#     return oldestDate


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


# Sort files by name
def sortFilesByName(files):
    # sortedFiles = sorted(files, key=lambda file:file.name) # sort by name
    sortedFiles = sorted(files) # sort by name

    return sortedFiles

# How is the best way
# 1 - re-name the files and re-sequence them - [doing this one]
# 2 - read the creation date and re-name then according to it
def reSequenceFiles(files):
    # get the first file name - [DONE]
    # get the numeration from the first file name
    # read the name of each file
    # get the subtext from the last "_" to the end
    #   example: "2024-01-20_event_001" gets "001"
    # re-sequence

    # only name
    firstFileName = ic(Path(files[0]).stem)

    # numeration


    for fileName in files:
      ic(fileName)


    # return sequencedFiles


# PROGRAM STARTS
# Gets the current working directory
currentPath = os.getcwd() + "/"

photoFiles = getNameFiles(PHOTO_TYPES) #returns an array with valid photo files
videoFiles = getNameFiles(VIDEO_TYPES) #returns an array with valid video files
# ic(photoFiles)

sortedFiles = sortFilesByName(photoFiles)
ic(sortedFiles)

reSequenceFiles(sortedFiles)

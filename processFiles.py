# Python3 ~/MyDocuments/DEV/Python/SourceCode/PhotoVideo/processFiles.py
# Python3 processFiles.py

# To re-name files after being processed
# It won't change dates, only numeration
# 2024-01-01_event_003.jpg
# 2024-01-02_event_005.jpg
# 2024-01-04_event_007.jpg
# To
# 2024-01-01_event_001.jpg
# 2024-01-02_event_002.jpg
# 2024-01-04_event_003.jpg

#TODO
# Read files from a folder, same folder, same date - [DONE]
# sort them by name - [DONE]
# Re-sequence them - [DONE]
# Pass by parameter a name and use it to replace 'event'

import os, shutil, glob
import exifread #pip install exifread
import os.path, time, datetime, calendar
from subprocess import check_output, check_call
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


# Sort files by name
def sortFilesByName(files):
    # sortedFiles = sorted(files, key=lambda file:file.name) # sort by name
    sortedFiles = sorted(files) # sort by name

    return sortedFiles


def getLenSequence(file):
  firstFileName = Path(file).stem # get file's name no extension
  lastUnderscore = firstFileName.rfind("_") # last underscore
  sequence = firstFileName[-(len(firstFileName)-lastUnderscore-1):] # gets sequence
  # newSequence = "".join(f'{1:0{len(sequence)}}') # gets new sequence

  return len(sequence)


def getRawFileName(file):
  fileName = Path(file).stem # get file's name no extension
  positionLastUnderscore = fileName.rfind("_") # last underscore

  return fileName[0:positionLastUnderscore + 1]

# How is the best way
# 1 - re-name the files and re-sequence them - [DONE]
# 2 - read the creation date and re-name them according to it
def reSequenceFiles(files):
  # gets new sequence
  lenSequence = getLenSequence(files[0])
  # ic(lenSequence)

  for i, file in enumerate(files, start=1):
    # --- SEEMS TO BE WORKING ---

    # name = os.path.splitext(file)[0]
    # ic(name)
    fileExtension = os.path.splitext(file)[1]
    # ic(fileExtension)

    try:
      newFileName = ''.join((getRawFileName(file), f'{i:0{lenSequence}}', fileExtension))
      # ic(newFileName)
      os.rename(file, newFileName)
    except:
      print(f"Rename operation failed: {getRawFileName(file)} --> {newFileName}")
      # sys.exit()


# PROGRAM STARTS
# Gets the current working directory
currentPath = os.getcwd() + "/"

photoFiles = getNameFiles(PHOTO_TYPES) #returns an array with valid photo files
videoFiles = getNameFiles(VIDEO_TYPES) #returns an array with valid video files
# ic(photoFiles)

sortedFiles = sortFilesByName(photoFiles)
# ic(sortedFiles)

reSequenceFiles(sortedFiles)

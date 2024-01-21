# Python3 ~/MyDocuments/DEV/Python/SourceCode/PhotoVideo/processFiles.py
# Python3 processFiles.py   |||   no name change, sorted by name
# Python3 processFiles.py new_name -d   |||   -d : sorted by date
# pF (it calls an alias with the command)

# To re-name files
# It won't change dates, only numeration and/or event name
# 2024-01-01_event_003.jpg
# 2024-01-02_event_005.jpg
# 2024-01-04_event_007.jpg
# To
# 2024-01-01_event_01.jpg
# 2024-01-02_event_02.jpg
# 2024-01-04_event_03.jpg
# It is working

#TODO
#
# Make it an exe
#   https://rohitsaroj7.medium.com/how-to-turn-your-python-script-into-an-executable-file-d64edb13c2d4

import os, glob, getopt
import os.path
import sys
from subprocess import check_output, check_call
from icecream import ic #pip install icecream
from pathlib import Path

# Photo and Video files extensions allowed
PHOTO_TYPES = ('*.dng', '*.DNG', '*.jpe', '*.JPE', '*.jpeg', '*.JPEG', '*.jpg', '*.JPG', '*.png', '*.PNG')
VIDEO_TYPES = ('*.mov', '*.MOV', '*.mp4', '*.MP4')

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


# Sort files by name or date
def sortFiles(files):
    if dateFlag:
      sortedFiles = sorted(files, key=os.path.getmtime) # based on creation date
    else:
      sortedFiles = sorted(files) # sort by name

    return sortedFiles


def getLenSequence(lenFiles):
  _secuence = "02"
  if lenFiles > 9999: _secuence = "04"
  elif lenFiles > 999: _secuence = "03"

  return _secuence


def getRawFileName(file, event):
  fileName = Path(file).stem # get file's name no extension
  result = ""

  if event :
     positionFirstUnderscore = fileName.find("_")
     result = fileName[0:positionFirstUnderscore + 1] + event + "_"
  else :
     positionLastUnderscore = fileName.rfind("_")
     result = fileName[0:positionLastUnderscore + 1]

  return result

# How is the best way
# 1 - re-name the files and re-sequence them - [DONE]
# 2 - read the creation date and re-name them according to it
def reSequenceFiles(files, newEvent):
  # gets new sequence length
  lenSequence = getLenSequence(len(files))
  numberFilesRenamed = 0

  for i, file in enumerate(files, start=1):
    fileExtension = os.path.splitext(file)[1]
    # ic(fileExtension)

    try:
      newFileName = ''.join((getRawFileName(file, newEvent), f'{i:0{lenSequence}}', fileExtension))
      if file != newFileName:
        numberFilesRenamed += 1
        os.rename(file, newFileName)
    except:
      print(f"Rename operation failed: {getRawFileName(file)} --> {newFileName}")
      # sys.exit()

  print(f"Files renamed: {numberFilesRenamed}")


# PROGRAM STARTS

# Reads command arguments
newEvent = ""
dateFlag = False
if len(sys.argv) > 1:
  newEvent = sys.argv[1]
  if len(sys.argv) > 2 and sys.argv[2] == "-d":
    dateFlag = True

# Gets the current working directory
currentPath = os.getcwd() + "/"

photoFiles = getNameFiles(PHOTO_TYPES) #returns an array with valid photo files
videoFiles = getNameFiles(VIDEO_TYPES) #returns an array with valid video files
# ic(photoFiles)

sortedFiles = sortFiles(photoFiles)
# ic(sortedFiles)

reSequenceFiles(sortedFiles, newEvent)

#Python3 setFolderNames.py
#To process folders and files (photos) from Sony camera, it will set the folder and file names
#ASSUMING dates on folders and files are correct

import os, shutil, glob
import exifread #pip install exifread
import os.path, time, calendar
from subprocess import check_output, check_call
 
# Current working directory
currentPath = os.getcwd() + "/"

#Only Folders
folders = next(os.walk(currentPath))[1] # for the current dir use ('.')
#print(listOfFolders)

for folder in folders:
    newFolderName = time.strftime('event_%b-%d', time.localtime(os.path.getmtime(currentPath + folder)))
    
    if newFolderName != '':
        #Rename folder
        os.rename(folder, newFolderName)
        #print(newFolderName)

        #Get files inside folder
        files = os.listdir(currentPath + "/" + newFolderName)

        for i, file in enumerate(files, start=1):
            #2021-01-31_event_001
            newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
            
            fileExtension = os.path.splitext(file)[1]

            newFileName = newFileName + fileExtension

            #Rename files
            os.rename(file, newFileName)
            #print(newFileName)

    else:
        print("DATE %s NOT VALID" % newFolderName)



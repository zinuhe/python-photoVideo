# Python3 setFolderNames.py
# To process folders and files (photos) from Sony camera, 
# it will set the folder and file names according to created date
# ASSUMING dates on folders and files are correct

import os, shutil, glob
import exifread #pip install exifread
import os.path, time, calendar
from subprocess import check_output, check_call
import sys
 
# Current working directory
currentPath = os.getcwd() + "/"

#Only Folders
folders = next(os.walk(currentPath))[1] # for the current dir use ('.')
folders.sort()
#print(folders)

for folder in folders:
    newFolderName = time.strftime('event_%b-%d', time.localtime(os.path.getctime(currentPath + folder)))
    
    print("folder: " + folder)
    print("newFolderName: " + newFolderName)

    sys.exit()

    if newFolderName != '':
        if newFolderName != folder:
            try:
                #Rename folder
                print("folder: " + folder)
                print("newFolderName: " + newFolderName)
                os.rename(folder, newFolderName)
            except OSError:
                    print("Rename folder operation fails for: " + folder + "/" + file + " --> " + folder + "/" + newFileName)
                    sys.exit()

        #Get files inside folder and sort them out
        files = os.listdir(currentPath + "/" + newFolderName)
        files.sort()

        for i, file in enumerate(files, start=1):
            #YYYY-MM-DD_event_001.ext
            #newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder))) + f'{i:03}'
            newFileName = time.strftime('%Y-%m-%d_event_', time.localtime(os.path.getmtime(currentPath + folder + "/" + file))) + f'{i:03}'
            
            fileExtension = os.path.splitext(file)[1]

            newFileName = newFileName + fileExtension

            if file != newFileName:
                #Rename files
                try:
                    os.rename(folder + "/" + file, folder + "/" + newFileName)
                except OSError:
                    print("Rename file operation fails for: " + folder + "/" + file + " --> " + folder + "/" + newFileName)
                    sys.exit()
                
                #print("file: " + folder + "/" + file)
                #print("newFileName: " + folder + "/" + newFileName)
    else:
        print("DATE %s NOT VALID" % newFolderName)


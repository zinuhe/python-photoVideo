#Copy files from _testFiles to root and delete /photo and /video
#Python3 reset.py
import os, shutil, glob
import exifread #pip install exifread
import os.path, time

# detect the current working directory
currentPath = os.getcwd() + "/"

sourcePath = currentPath + "_testFiles"


photoPath = currentPath + "photo"
videoPath = currentPath + "video"

def copytree(source, destination, symlinks=False, ignore=None):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

copytree(sourcePath, currentPath)

#Delete photo and video folders
shutil.rmtree(photoPath, ignore_errors=False, onerror=None)
shutil.rmtree(videoPath, ignore_errors=False, onerror=None)


#from distutils.dir_util import copy_tree
#copy_tree("/a/b/c", "/x/y/z")


# try: 
#     shutil.copy(sourcePath+"/IMG_1436.JPG", destinationPath)
#     #print("File copied successfully.") 
  
# # If source and destination are same 
# except shutil.SameFileError: 
#     print("Source and destination represents the same file.") 
  
# # If there is any permission issue 
# except PermissionError: 
#     print("Permission denied.") 
  
# # For other errors 
# except: 
#     print("Error occurred while copying file.") 



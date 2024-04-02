# Python-PhotoVideo

## processPhotoVideo.py

To process photo and video files under same folder, by example files from iPhone.

## processPhotoVideoSony.py

To process folders and files (photos) from Sony camera and drone.
It will set the folder and file names according to the `date` from EXIF info
ASSUMING dates on folders and files are correct.

## processFolderDates.py

Given a list of folders, it goes inside each one gets the earlies file date and then set up the folder's creation date with that date.

Works with pictures and videos because it uses inside files' creation dates rather than EXIF info.

Files shoud have propertly set up creation date.

## processFiles.py
Rename files

It won't change dates, only numeration and/or event name

2024-01-01_event_003.jpg
2024-01-02_event_005.jpg
2024-01-04_event_007.jpg
To
2024-01-01_event_01.jpg
2024-01-02_event_02.jpg
2024-01-04_event_03.jpg

## To check

[Ice cream](https://towardsdatascience.com/introducing-icecream-never-use-print-to-debug-your-python-code-again-d8f2e5719f8a)

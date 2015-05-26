__author__ = 'Michael'
import exifread
import os

disk = input("Type a drive letter to search for exif data:" + "\n")
path = disk + ":\\"

for root, subdirs, files in os.walk(path):
    for file in files:
        if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.tif', '.tiff'):
            path_name = (os.path.join(root, file))
            f = open(path_name, 'rb')
            tags = exifread.process_file(f)
            if not tags:
                pass
            else:
                print(path_name, tags)
import exifread
import exifconvert
import os

# User input

disk = input("Type a drive letter to search for exif data:" + "\n")
path = disk + ":\\"
#Search jpg and tiff recursively
for root, subdirs, files in os.walk(path):
    for file in files:
        if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.tif', '.tiff'):
            #Path to file
            path_name = (os.path.join(root, file))
            data = open(path_name, 'rb')
            tags = exifread.process_file(data, 'UNDEF', False, False, False)
            if not tags:
                pass
            else:
                #Latitude, Longitude, Altitude coordinates for the picture
                #
                # print(exifconvert.GetGps(tags))
                try:
                    print("Location data and filepath: ", exifconvert.GetGps(tags), path_name)
                except KeyError:
                    print("This file has no location data: ",path_name)
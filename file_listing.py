from os import listdir
from os.path import isfile, join

path = raw_input("Path: ")

just_files = [f for f in listdir(path) if isfile(join(path,f))]
print(just_files)
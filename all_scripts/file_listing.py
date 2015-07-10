from os import listdir
from os.path import isfile, join

# path = raw_input("Path: ")
path = '/Users/Bart/Downloads'

just_files = [f for f in listdir(path) if isfile(join(path,f))]

for i in just_files:
    print i

print(just_files)

import os
import os.path as osp

def hash():

    ROOT = raw_input("Enter the full-path to the folder or drive to index \n")

    def write(text):
        print(text)

    write("Full paths and filenames.." + "\n")
    for root, dirs, files in os.walk(ROOT):
        for fpath in [osp.join(root, f) for f in files]:
            name = osp.relpath(fpath, ROOT)

            write('%s' % ( name))
            with open("tree_hierarchy.txt", "a") as hashes:
                hashes.write('%s' % (name) + '\n')

if __name__ == '__main__':
    hash()
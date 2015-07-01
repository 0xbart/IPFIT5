import os
import os.path as osp
import hashlib

def hash():
    def filehash(filepath):
        blocksize = 64*1024
        sha = hashlib.sha256()
        with open(filepath, 'rb') as fp:
            while True:
                data = fp.read(blocksize)
                if not data:
                    break
                sha.update(data)
        return sha.hexdigest()

    ROOT = raw_input("""Which folder would you like to hash? Choose "." for current. \n""")

    def write(text):
        print(text)

    write("""File hasher 0.1 | SIZE | SHA256 | Path & filename """)
    for root, dirs, files in os.walk(ROOT):
        for fpath in [osp.join(root, f) for f in files]:
            size = osp.getsize(fpath)
            sha = filehash(fpath)
            name = osp.relpath(fpath, ROOT)

            write('%s, %s, %s' % (size, sha, name))
            with open("hashes.txt", "a") as hashes:
                hashes.write('%s, %s, %s' % (size, sha, name) + '\n')

if __name__ == '__main__':
    hash()
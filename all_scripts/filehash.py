import os
import os.path as osp
import hashlib
import sqlite3

def scanComputerHashes(casename, eName):
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
        # dir = /Users/Bart/Downloads/folder-tree-static

        def write(text):
            pass

        write("""File hasher 0.1 | SIZE | SHA256 | Path & filename """)

        countFiles = 0
        allFiles = []

        for root, dirs, files in os.walk(ROOT):
            for fpath in [osp.join(root, f) for f in files]:
                size = osp.getsize(fpath)
                sha = filehash(fpath)
                name = osp.relpath(fpath, ROOT)

                allFiles.append([])
                allFiles[countFiles].append(('size', size))
                allFiles[countFiles].append(('sha', sha))
                allFiles[countFiles].append(('name', name))

                countFiles = countFiles + 1

                write('%s, %s, %s' % (size, sha, name))
                with open("hashes.txt", "a") as hashes:
                    hashes.write('%s, %s, %s' % (size, sha, name) + '\n')


        db = sqlite3.connect(casename)
        cursor = db.cursor()
        for i in range(len(allFiles)):
            print 'het werkt!'
            cursor.execute('INSERT INTO `' + eName + '_files` ('
                           'name, size, shahash) '
                           'VALUES (?,?,?)',
                           (allFiles[i][2][1],
                            allFiles[i][0][1],
                            allFiles[i][1][1]))

        db.commit()

    if __name__ == '__main__':
        hash()

scanComputerHashes('db/cases/stijn.db', 'pc')

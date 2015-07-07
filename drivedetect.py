__author__ = 'Michael'
import re
import psutil

def driveinfoWinUnix():
#Cross platform schijf info
    diskinfo = str(psutil.disk_partitions())
    for match in re.findall('[A-Z]{1}[:]{1}|[/][d][e][v][/][a-z]{3,4}[0-9]{0,2}[a-z]{0,2}[0-9]|[N][T][F][S]|[n][t][f][s]|[e][x][t][2-4]|[e]{0,1}[x]{0,1}[F][A][T]|[h][f][s]|[R][e][F][S]', diskinfo):
        print match

driveinfoWinUnix()
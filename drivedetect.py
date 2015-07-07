__author__ = 'Michael'
import re
import psutil

def driveinfoWinUnix():
#Cross platform schijf info
    diskinfo = str(psutil.disk_partitions())
    print diskinfo
    for match in re.findall( r'[A-Z]{1}[:]{1}|[/][dev][/][a-z]{4}[0-9]{2}|[/][d][e][v][/][a-z]{3}[0-9]{0,2}|[A-Z]{2,4}|[d][e][v][/][a-z]{3}[0-9]{0,2}|[e][x][t][2-4]|[e]{0,1}[x]{0,1}[F][A][T]|[h][f][s]|[R][e][F][S]', diskinfo):
        print match
#Split voor aantal aanwezige schijven


driveinfoWinUnix()
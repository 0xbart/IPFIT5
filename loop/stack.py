from dirtools import Dir
from os import listdir
from os.path import isfile, join
import os.path
import os

path = '/Users/Bart/Downloads/folder-tree-static/_TEST/zzz'


def createHTMLFiles(d):
    html = ''

    try:
        files = [f for f in listdir(d) if isfile(join(d,f))]

        for file in files:
            html += '<li class="dhtmlgoodies_sheet.gif"><a href="#">' + file + '</a></li>'
    except:
        pass

    return html


def createHTML(d, first):
    if first:
        res = ''
    else:
        res = '<ul>'

    lds = os.listdir(d)

    for l in lds:
        if os.path.isdir(os.path.join(d,l)):
            res += '<li><a href="#">' + l + '</a>'
            res += createHTML(os.path.join(d,l), False)
            if not first:
                res += createHTMLFiles(d)
            res += '</li>'

    if first:
        res += createHTMLFiles(path)
    res += '</ul>'
    html = res.replace('<ul></ul>', '')

    return html


html = '<html><head><title>Pythronic tree dirs and files</title>'
html += '<link rel="stylesheet" href="css/folder-tree-static.css" type="text/css">'
html += '<link rel="stylesheet" href="css/context-menu.css" type="text/css">'
html += '<script type="text/javascript" src="js/ajax.js"></script>'
html += '<script type="text/javascript" src="js/folder-tree-static.js"></script>'
html += '<script type="text/javascript" src="js/context-menu.js"></script>'
html += '</head><body><ul id="dhtmlgoodies_tree" class="dhtmlgoodies_tree">'
html += createHTML(path, True)
html += '<a href="#" onclick="expandAll(\'dhtmlgoodies_tree\');return false">Expand all</a> '
html += '<a href="#" onclick="collapseAll(\'dhtmlgoodies_tree\');return false">Collapse all</a>'
html += '</body></html>'

logfile = open('loop.html', 'w')
logfile.write(html)
logfile.close()

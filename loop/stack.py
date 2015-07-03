from dirtools import Dir
import os.path
import os

path = 'D:\Documents'


def getHTMLItems(d, l):
    html = ''
    tmppath = d + '/' + l

    if not tmppath == path:
        d = Dir(tmppath, exclude_file='.gitignore')

        files = d.files()
        for file in files:
        	html += '<li class="dhtmlgoodies_sheet.gif"><a href="#">' + file + '</a></li>'
    else:
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
            res += '</li>'
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

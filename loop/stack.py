from dirtools import Dir
from os import listdir
from os.path import isfile, join
import os.path
import os

path = 'enter path'
slash = '/'


def createHTMLFiles(d):
    html = ''

    extImg = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
    extVideo = ['.avi', '.mp4', '.mkv']
    extWord = ['.doc', '.docx', '.dot', 'dotx']
    extExcel = ['.xls', '.xlsx', '.xlt', '.xltx']
    extPower = ['.ppt', '.pptx', '.pot', '.pps', '.potx', 'ppsx']
    extExe = ['.exe']
    extMail = ['.pst']
    extPdf = ['.pdf']
    extRar = ['.rar']
    extZip = ['.zip']
    extText = ['.txt', '.log']

    try:
        files = [f for f in listdir(d) if isfile(join(d,f))]

        for file in files:
            ext = os.path.splitext(file)[1]
            ext = ext.lower()

            if ext in extImg:
                html += '<li class="dhtmlgoodies_photo.gif"><a href="#">' + file + '</a></li>'
            elif ext in extVideo:
                html += '<li class="dhtmlgoodies_video.gif"><a href="#">' + file + '</a></li>'
            elif ext in extWord:
                html += '<li class="dhtmlgoodies_word.gif"><a href="#">' + file + '</a></li>'
            elif ext in extExcel:
                html += '<li class="dhtmlgoodies_excel.gif"><a href="#">' + file + '</a></li>'
            elif ext in extPower:
                html += '<li class="dhtmlgoodies_power.gif"><a href="#">' + file + '</a></li>'
            elif ext in extExe:
                html += '<li class="dhtmlgoodies_exe.gif"><a href="#">' + file + '</a></li>'
            elif ext in extMail:
                html += '<li class="dhtmlgoodies_mail.gif"><a href="#">' + file + '</a></li>'
            elif ext in extPdf:
                html += '<li class="dhtmlgoodies_pdf.gif"><a href="#">' + file + '</a></li>'
            elif ext in extRar:
                html += '<li class="dhtmlgoodies_rar.gif"><a href="#">' + file + '</a></li>'
            elif ext in extZip:
                html += '<li class="dhtmlgoodies_zip.gif"><a href="#">' + file + '</a></li>'
            elif ext in extText:
                html += '<li class="dhtmlgoodies_txt.gif"><a href="#">' + file + '</a></li>'
            else:
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

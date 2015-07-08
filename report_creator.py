import sqlite3

iconOk = '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
iconRemove = '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'

db = sqlite3.connect('db/cases/Bart.db')
cursor = db.cursor()

cursor.execute('''SELECT id, name, description, type, created_at, deleted FROM evidences''')
fetchEvidences = cursor.fetchall()

cursor.execute('''SELECT id, name, description, created_at FROM general''')
fetchGeneral = cursor.fetchall()

html = ''
html += '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Pythronic - Report</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="bootstrap/css/font-awesome.min.css" />
    <script type="text/javascript" src="bootstrap/js/jquery-1.10.2.min.js"></script>
    <script type="text/javascript" src="bootstrap/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
    <div class="page-header">
        <h1>Pythronic <small>Report</small></h1>
    </div>
    <div class="container">
    <div class="alert alert-warning alert-dismissible" role="alert">
        <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        Dit is het automatisch gerenegeerde testrapport. Bekijk de resultaten in de uitklapbare lijsten.
    </div>
    <div class="panel-group" id="accordion">
    <div class="faqHeader">Case</div>
    <div class="panel panel-default">
    <div class="panel-heading">
        <h4 class="panel-title">
        <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseOne"> Bewijsmateriaal</a>
        </h4>
    </div>
    <div id="collapseOne" class="panel-collapse collapse">
    <div class="panel-body">
        <table class="table">
        <tr>
            <th>ID</th>
            <th>Naam</th>
            <th>Beschrijving</th>
            <th>Type</th>
            <th>Aangemaakt op:</th>
            <th>Verwijderd</th>
        </tr>
'''

for row in fetchEvidences:
    html += ('<tr>')
    html += ('<td>{0}</td><td>{1}</td><td>{2}<td>{3}<td>{4}<td>{5}'
              .format(row[0],
                      row[1],
                      row[2] if row[2] != '' else '-',
                      row[3],
                      row[4],
                      'Ja' if row[5] == '1' else 'Nee') + '</td>')
    html += ('</tr>')

html += '''
        </table>
    </div>
    </div>
    </div>
    <div class="panel panel-default">
    <div class="panel-heading">
        <h4 class="panel-title">
        <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">Algemeen</a>
        </h4>
    </div>
    <div id="collapseTwo" class="panel-collapse collapse">
    <div class="panel-body">
        <table class="table">
        <tr>
            <th>ID</th>
            <th>Naam</th>
            <th>Beschrijving</th>
            <th>Aangemaakt op</th>
            </tr>
'''

for row in fetchGeneral:
     html += ('<tr>')
     html += ('<td>{0}</td><td>{1}</td><td>{2}<td>{3}'
              .format(row[0],
                      row[1],
                      row[2] if row[2] != '' else '-',
                      row[3]) + '</td>')
     html += ('</tr>')


html += '''
        </table>
    </div>
    </div>
    </div>
<div class="faqHeader">Modules</div>
<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseThree"> \
Hardware info</a>
</h4></div>
<div id="collapseThree" class="panel-collapse collapse">
<div class="panel-body">
<table class="table">
<tr><th>ID</th><th>CPU</th><th>USB Devices</th><th>Architectuur</th><th>CPU Naam</th><th>CPU Family</th><th>Gebruikte Geheugen</th><th>Vrije Geheugen</th><th>Totaal Geheugen</th></tr>'''

cursor.execute('''SELECT id, processor, usb_devices, system_arch, proc_name, proc_family, used_memory, free_memory, total_memory FROM PC_hardware''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}''</td> ' '<td>' '{1}' '</td> ' '<td>' '{2}' '<td>' '{3}' '<td>' '{4}' '<td>' '{5}' '<td>' '{6}' '<td>' '{7}' '<td>' '{8}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) + '</td>')
     html += ('</tr>')


html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseFour"> \
Software lijst</a>
</h4></div>
<div id="collapseFour" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Naam</th></tr>'''

cursor.execute('''SELECT id, name FROM PC_software''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}''</td> ' '<td>' '{1}'.format(row[0], row[1]) + '</td>')
     html += ('</tr>')


html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseFive"> \
Cloud gebruik</a>
</h4></div>
<div id="collapseFive" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Dropbox</th><th>OneDrive</th><th>Evernote</th><th>Google Drive</th></tr>'''

cursor.execute('''SELECT id, dropbox, onedrive, evernote, googledrive FROM PC_cloud''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>{0}</td><td>{1}<td>{2}<td>{3}<td>{4}'
              .format(row[0],
                      iconOk if row[1] == 1 else iconRemove,
                      iconOk if row[2] == 1 else iconRemove,
                      iconOk if row[3] == 1 else iconRemove,
                      iconOk if row[4] == 1 else iconRemove,) + '</td>')
     html += ('</tr>')


html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseSix"> \
Browser history</a>
</h4></div>
<div id="collapseSix" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Chrome</th><th>FireFox</th><th>Internet Explorer</th></tr>'''

cursor.execute('''SELECT id, his_chrome, his_ff, his_iexplorer FROM PC_browser''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}' '<td>' '{2}' '<td>' '{3}'.format(row[0], row[1], row[2], row[3]) + '</td>')
     html += ('</tr>')


html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseSeven"> \
Detected drives</a>
</h4></div>
<div id="collapseSeven" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Drive Naam:</th><th>Drive Mount:</th><th>Drive filesystem:</th></tr>'''

cursor.execute('''SELECT id, drive_name, drive_mountpoint, drive_filesystem FROM PC_drive''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}' '<td>' '{2}'.format(row[0], row[1], row[2]) + '</td>')
     html += ('</tr>')


html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseEight"> \
File hashing</a>
</h4></div>
<div id="collapseEight" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Bestandsnaam:</th><th>Parent:</th><th>SHA-hash:</th><th>MD5-hash:</th></tr>'''

cursor.execute('''SELECT id, name, size, shahash, md5hash FROM PC_files''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}' '<td>' '{2}' '<td>' '{3}' '<td>' '{4}'.format(row[0], row[1], row[2], row[3], row[4]) + '</td>')
     html += ('</tr>')


html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseNine"> \
Linux login items</a>
</h4></div>
<div id="collapseNine" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Naam</th></tr>'''

cursor.execute('''SELECT id, name FROM PC_linux_logon''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}'.format(row[0], row[1]) + '</td>')
     html += ('</tr>')

html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseTen"> \
Detected users</a>
</h4></div>
<div id="collapseTen" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Naam</th></tr>'''

cursor.execute('''SELECT id, name FROM PC_users''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}'.format(row[0], row[1]) + '</td>')
     html += ('</tr>')

html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseEleven"> \
Windows startup applications</a>
</h4></div>
<div id="collapseEleven" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Naam</th></tr>'''

cursor.execute('''SELECT id, name FROM PC_win_logon''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}'.format(row[0], row[1]) + '</td>')
     html += ('</tr>')

html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseTwelve"> \
Virus Total</a>
</h4></div>
<div id="collapseTwelve" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>Virus naam</th><th>Virus hash</th><th>Details</th></tr>'''

cursor.execute('''SELECT id, virus_name, virus_hash, virus_output FROM PC_virus''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}' '<td>' '{2}' '<td>' '{3}'.format(row[0], row[1], row[2], row[3]) + '</td>')
     html += ('</tr>')

html += '''
</table>
</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">

<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseThirteen"> \
Networking details</a>
</h4></div>
<div id="collapseThirteen" class="panel-collapse collapse">
<div class="panel-body">'''
html += '''
<table class="table">
<tr><th>ID</th><th>IP</th><th>MAC</th><th>IP Connected:</th></tr>'''

cursor.execute('''SELECT id, ip, mac, connected_ip FROM PC_network''')
table = cursor.fetchall() #retrieve the first row

for row in table:
     html += ('<tr>')
     html += ('<td>' '{0}' '</td> ' '<td>' '{1}' '<td>' '{2}' '<td>' '{3}'.format(row[0], row[1], row[2], row[3]) + '</td>')
     html += ('</tr>')

html += '''
</table>
</div>
</div>
</div>'''

html += """<style>
    .faqHeader {
        font-size: 27px;
        margin: 20px;
    }

    .panel-heading [data-toggle="collapse"]:after {
        font-family: 'Glyphicons Halflings';
        content: "\e072"; /* "play" icon */
        float: right;
        color: #F58723;
        font-size: 18px;
        line-height: 22px;
        /* rotate "play" icon from > (right arrow) to down arrow */
        -webkit-transform: rotate(-90deg);
        -moz-transform: rotate(-90deg);
        -ms-transform: rotate(-90deg);
        -o-transform: rotate(-90deg);
        transform: rotate(-90deg);
    }

    .panel-heading [data-toggle="collapse"].collapsed:after {
        /* rotate "play" icon from > (right arrow) to ^ (up arrow) */
        -webkit-transform: rotate(90deg);
        -moz-transform: rotate(90deg);
        -ms-transform: rotate(90deg);
        -o-transform: rotate(90deg);
        transform: rotate(90deg);
        color: #454444;
    }
</style>"""

html += '</div>'
html += '</body>'
html += '</html>'


file = open('report.html', 'w')
file.write(html)
file.close()

import sqlite3


def makeRapport():
    result = False

    try:
        iconOk = ('<span class="glyphicon glyphicon-ok" aria-hidden="true">'
                  '</span>')
        iconRemove = ('<span class="glyphicon glyphicon-remove"'
                      'aria-hidden="true"></span>')

        db = sqlite3.connect('db/cases/Bart.db')
        cursor = db.cursor()

        cursor.execute('''SELECT id, name, description, type, created_at, deleted
                          FROM evidences''')
        fetchEvidences = cursor.fetchall()

        cursor.execute('''SELECT id, name, description, created_at
                          FROM general''')
        fetchGeneral = cursor.fetchall()

        cursor.execute('''SELECT id, processor, usb_devices, system_arch,
                          proc_name, proc_family, used_memory, free_memory,
                          total_memory FROM PC_hardware''')
        fetchHardware = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM PC_software''')
        fetchSoftware = cursor.fetchall()

        cursor.execute('''SELECT id, dropbox, onedrive, evernote, googledrive
                          FROM PC_cloud''')
        fetchCloud = cursor.fetchall()

        cursor.execute('''SELECT id, his_chrome, his_ff, his_iexplorer
                          FROM PC_browser''')
        fetchBrowser = cursor.fetchall()

        cursor.execute('''SELECT id, drive_name, drive_mountpoint, drive_filesystem
                           FROM PC_drive''')
        fetchDrive = cursor.fetchall()

        cursor.execute('''SELECT id, name, size, shahash, md5hash
                          FROM PC_files''')
        fetchFiles = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM PC_linux_logon''')
        fetchLinuxLogin = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM PC_win_logon''')
        fetchWindowsLogon = cursor.fetchall()

        cursor.execute('''SELECT id, ip, mac, connected_ip
                          FROM PC_network''')
        fetchNetwork = cursor.fetchall()

        #  START START HTML

        html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8" />
                <title>Pythronic - Report</title>
                <meta name="viewport" content="width=device-width,
                initial-scale=1.0" />
                <link rel="stylesheet" type="text/css"
                href="bootstrap/css/bootstrap.min.css" />
                <link rel="stylesheet" type="text/css"
                href="bootstrap/css/font-awesome.min.css" />
                <script type="text/javascript"
                src="bootstrap/js/jquery-1.10.2.min.js"></script>
                <script type="text/javascript"
                src="bootstrap/js/bootstrap.min.js"></script>
            </head>
        '''

        #  END START HMLT

        #  START HTML BODY
        html += '''
            <body>
                <div class="container">
                <div class="page-header">
                    <h1>Pythronic <small>Report</small></h1>
                </div>
                <div class="container">
                <div class="alert alert-info alert-dismissible" role="alert">
                    <button type="button" class="close" data-dismiss="alert">
                    <span aria-hidden="true">&times;</span>
                    <span class="sr-only">Close</span></button>
                    Dit is het automatisch gerenegeerde rapport.
                    Bekijk de resultaten in de uitklapbare lijsten.
                </div>
                <div class="panel-group" id="accordion">
                <div class="faqHeader">Case</div>
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseOne"> Bewijsmateriaal</a>
                    </h4>
                </div>
                <div id="collapseOne" class="panel-collapse collapse">
                <div class="panel-body">
                    <table class="table table-hover">
                    <tr>
                        <th>ID</th>
                        <th>Naam</th>
                        <th>Beschrijving</th>
                        <th>Type</th>
                        <th>Aangemaakt op</th>
                        <th>Verwijderd</th>
                    </tr>
        '''

        for row in fetchEvidences:
            html += ('<tr>')
            html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                     '<td>{4}</td><td>{5}</td>'
                     .format(row[0],
                             row[1],
                             row[2] if row[2] != '' else '-',
                             'PC / Laptop / Server' if str(row[3]) == '1'
                             else 'Device (USB, SD, HDD)',
                             row[4],
                             'Ja' if str(row[5]) == '1' else 'Nee'))
            html += ('</tr>')

        html += '''
            </table>
            </div>
            </div>
            </div>
            <div class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a class="accordion-toggle collapsed"
                    data-toggle="collapse" data-parent="#accordion"
                    href="#collapseTwo">Algemeen</a>
                </h4>
            </div>
            <div id="collapseTwo" class="panel-collapse collapse">
            <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                    <th>Beschrijving</th>
                    <th>Aangemaakt op</th>
                </tr>
        '''

        for row in fetchGeneral:
            html += ('<tr>')
            html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                     .format(row[0],
                             row[1],
                             row[2] if row[2] != '' else '-',
                             row[3]))
            html += ('</tr>')

        html += '''
            </table>
            </div>
            </div>
            </div>
        '''

        #  END BODY HTML
        #  START IF HARDWARE

        if fetchHardware:
            html += '''
                <div class="faqHeader">Modules</div>
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseThree">Hardware info</a>
                    </h4>
                </div>
                <div id="collapseThree" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>CPU</th>
                    <th>USB Devices</th>
                    <th>Architectuur</th>
                    <th>CPU Naam</th>
                    <th>CPU Family</th>
                    <th>Gebruikte Geheugen</th>
                    <th>Vrije Geheugen</th>
                    <th>Totaal Geheugen</th>
                </tr>
            '''

            for row in fetchHardware:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         '<td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td>'
                         '<td>{8}</td>'
                         .format(row[0],
                                 iconRemove if str(row[1]) == 'None'
                                 else row[1],
                                 iconRemove if str(row[2]) == 'None'
                                 else row[2],
                                 iconRemove if str(row[3]) == 'None'
                                 else row[3],
                                 iconRemove if str(row[4]) == 'None'
                                 else row[4],
                                 iconRemove if str(row[5]) == 'None'
                                 else row[5],
                                 iconRemove if str(row[6]) == 'None'
                                 else row[6],
                                 iconRemove if str(row[7]) == 'None'
                                 else row[7],
                                 iconRemove if str(row[8]) == 'None'
                                 else row[8]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF HARDWARE
        #  START IF SOFTWARE

        if fetchSoftware:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseFour">Software lijst</a>
                    </h4>
                </div>
                <div id="collapseFour" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchSoftware:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0], row[1]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF SOFTWARE
        #  START IF CLOUD

        if fetchCloud:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseFive">Cloud gebruik</a>
                    </h4>
                </div>
                <div id="collapseFive" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Dropbox</th>
                    <th>OneDrive</th>
                    <th>Evernote</th>
                    <th>Google Drive</th>
                </tr>
            '''

            for row in fetchCloud:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td>'
                         '<td>{3}</td><td>{4}</td>'
                         .format(row[0],
                                 iconOk if str(row[1]) == '1' else iconRemove,
                                 iconOk if str(row[2]) == '1' else iconRemove,
                                 iconOk if str(row[3]) == '1' else iconRemove,
                                 iconOk if str(row[4]) == '1' else iconRemove))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF CLOUD
        #  START IF BROWSER

        if fetchBrowser:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseSix">Browser history</a>
                    </h4>
                </div>
                <div id="collapseSix" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Chrome</th>
                    <th>FireFox</th>
                    <th>Internet Explorer</th>
                </tr>
            '''

            for row in fetchBrowser:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         .format(row[0],
                                 iconOk if str(row[1]) == '1' else iconRemove,
                                 iconOk if str(row[2]) == '1' else iconRemove,
                                 iconOk if str(row[3]) == '1'
                                 else iconRemove,))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>'''

        #  END IF BROWSER
        #  START IF DRIVES

        if fetchDrive:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseSeven">Detected drives</a>
                    </h4>
                </div>
                <div id="collapseSeven" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Drive Naam</th>
                    <th>Drive Mount</th>
                    <th>Drive filesystem</th>
                </tr>
            '''

            for row in fetchDrive:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         .format(row[0],
                                 row[1],
                                 row[2],
                                 row[3]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF DRIVES
        #  START IF FILE HASH

        if fetchFiles:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseEight">File hashing</a>
                    </h4>
                </div>
                <div id="collapseEight" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Bestandsnaam</th>
                    <th>Size</th>
                    <th>SHA</th>
                    <th>MD5</th></tr>
            '''

            for row in fetchFiles:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td>'
                         '<td>{3}</td><td>{4}</td>'
                         .format(row[0],
                                 row[1],
                                 row[2],
                                 row[3],
                                 iconRemove if str(row[4]) == 'None'
                                 else row[4]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF FILE HASH
        #  IF LINUX LOGON

        if fetchLinuxLogin:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseNine">Linux login items</a>
                    </h4>
                </div>
                <div id="collapseNine" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchLinuxLogin:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0], row[1]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF LINUX LOGON
        #  START WINDOWS LOGON

        if fetchWindowsLogon:
            html == '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseEleven">Windows startup applications</a>
                    </h4>
                </div>
                <div id="collapseEleven" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchWindowsLogon:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0],
                                 row[1]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF LINUX LOGON
        #  START IF NETWORK

        if fetchNetwork:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseThirteen">Networking details</a>
                    </h4>
                </div>
                <div id="collapseThirteen" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>IP</th>
                    <th>MAC</th>
                    <th>IP Connected</th>
                </tr>
            '''

            for row in fetchNetwork:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         .format(row[0], row[1],
                                 iconRemove if str(row[2]) == 'None'
                                 else row[2],
                                 iconRemove if str(row[3]) == 'None'
                                 else row[3]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF NETWORK
        #  START BAR STYLING

        html += '''
            <style>
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
                    -webkit-transform: rotate(90deg);
                    -moz-transform: rotate(90deg);
                    -ms-transform: rotate(90deg);
                    -o-transform: rotate(90deg);
                    transform: rotate(90deg);
                    color: #454444;
                }
            </style>
        '''

        #  END BAR STYLING
        #  START END HTML

        html += '''
            </div>
            </body>
            </html>
        '''

        #  END END HTML

        file = open('report.html', 'w')
        file.write(html)
        file.close()

        result = True
    except:
        pass

    return result


if makeRapport():
    print 'Rapport gemaakt!'

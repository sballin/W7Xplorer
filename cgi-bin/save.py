#!/usr/bin/env python

import os
import cgi
import time
import glob

fs = cgi.FieldStorage()
saveName = '../datGUIconfig.json'
if glob.glob(saveName):
    os.rename(saveName, '../backups/datGUIconfig_{}.json'.format(int(time.time())))
with open(saveName, 'w') as f:
    f.write(str(fs.getvalue('text')))
os.system('chmod 777 {}'.format(saveName))


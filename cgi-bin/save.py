#!/usr/bin/env python

import os
import cgi
import time
import glob

fs = cgi.FieldStorage()

saveName = '../datGUIconfig.json'

if glob.glob(saveName):
    os.rename(saveName, '../datGUIconfig_backup_{}.json'.format(int(time.time())))
    
with open(saveName, 'w') as f:
    f.write(fs.getvalue('text'))

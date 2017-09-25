#!/usr/bin/env python

import sys
import os
import cgi
import time
import glob
import subprocess

fs = cgi.FieldStorage()
saveName = '../datGUIconfig.json'
if glob.glob(saveName):
    backupName = '../backups/datGUIconfig_{}.json'.format(int(time.time()))
    os.rename(saveName, backupName)
with open(saveName, 'w') as f:
    f.write(str(fs.getvalue('text')))
os.system('chmod 777 {}'.format(saveName))
diff = subprocess.Popen(['diff', '-U', '0', backupName, saveName], stdout=subprocess.PIPE).communicate()[0]
if not diff:
    diff = 'Save completed succesfully but no real changes were made.'

sys.stdout.write('Content-Type: application/plain\n\n')
sys.stdout.write('Save completed successfully. Comparison of backed up settings and most recently saved settings:\n\n{}'.format(diff))
sys.stdout.write('\n')
sys.stdout.close()

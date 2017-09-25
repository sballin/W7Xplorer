#!/usr/bin/env python

import sys
import os
import cgi
import pexpect
import json

fs = cgi.FieldStorage()
config = str(fs.getvalue('config'))
x = float(fs.getvalue('x'))
y = float(fs.getvalue('y'))
z = float(fs.getvalue('z'))

with open('key') as f:
    key = f.read()
    key = key.split('\n')[0]
    
base_url = 'http://svvmec1.ipp-hgw.mpg.de:8080/vmecrest/v1/geiger/w7x/'
config_dict = {'A_standard_beta-0':        '1000_1000_1000_1000_+0000_+0000/01/00jh_l/',
               'A_standard_beta-0.056':    '1000_1000_1000_1000_+0000_+0000/01/32/',
               'B-low-iota_beta-0':        '1000_1000_1000_1000_+0750_+0750/01/00/',
               'B_low-iota_beta-0.021':    '1000_1000_1000_1000_+0750_+0750/01/10ss/',
               'C_high-iota_beta-0':       '1000_1000_1000_1000_-0690_-0690/01/00/',
               'C_high-iota_beta-0.021':   '1000_1000_1000_1000_-0690_-0690/01/10s/',
               'D_low-mirror_beta-0':      '1042_1042_1127_1127_+0000_+0000/01/00/',
               'D_low-mirror_beta-0.043':  '1042_1042_1127_1127_+0000_+0000/01/20/',
               'E_high-mirror_beta-0':     '0972_0926_0880_0852_+0000_+0000/01/00jh/',
               'E_high-mirror_beta-0.053': '0972_0926_0880_0852_+0000_+0000/01/24a/'}

ps = pexpect.spawn("ssh jter@gate.rzg.mpg.de -t \"( curl '{}{}magneticfield.json?x={}&y={}&z={}' )\"".format(base_url, config_dict[config], x, y, z))
ps.expect('Are you sure you want to continue connecting (yes/no)?')
ps.sendline('yes')
ps.expect('Password:')
ps.sendline(key)
server_output = ps.read()

result = {}
result['message'] = 'The point on the LCFS closest to the chord end (endXYZ) was found (closestLCFSpoint) and marked with a blue sphere. This point is used to get the magnetic field vector (Bdirection).\n\nResponse from IPP server (for debugging purposes only): {}'.format(server_output)
server_output_json = json.loads(server_output.split('Connection')[0].split('\n')[1])
B = server_output_json['magneticField']
result['data'] = [B['Bx'][0], B['By'][0], B['Bz'][0]]

sys.stdout.write('Content-Type: application/json\n\n')
sys.stdout.write(json.dumps(result, indent=1))
sys.stdout.write('\n')
sys.stdout.close()

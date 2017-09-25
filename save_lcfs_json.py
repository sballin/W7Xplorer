import numpy as np
import urllib.request
import json
    
toroidal_angles = [round(t, 5) for t in np.arange(0, 2*np.pi, 0.025).tolist()]
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
           
for config_name, config_url in config_dict.items():
    print(config_name)
    lcfs_rs = []
    lcfs_zs = []
    for i, phi in enumerate(toroidal_angles):
        with urllib.request.urlopen(base_url + config_url + 'lcfs.json?phi=' + str(round(phi*180/np.pi, 5))) as url:
            data = json.loads(url.read().decode())
            lcfs_rs.extend(list(data['lcfs'][0]['x1']))
            lcfs_zs.extend(list(data['lcfs'][0]['x3']))
        print(i)
            
    lcfs_rs = [round(l, 5) for l in lcfs_rs]
    lcfs_zs = [round(l, 5) for l in lcfs_zs]

    with open('lcfs_{}.json'.format(config_name), 'w') as f:
        f.write(json.dumps({"name": config_name, "r": lcfs_rs, "z": lcfs_zs, "phi": toroidal_angles}, separators=(',', ':')))

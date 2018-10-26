import numpy as np
import urllib.request
import json
    
    
def saveLCFSjson():
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


def saveDivertorJson():
    ids = [170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309]
    base_url = 'http://esb.ipp-hgw.mpg.de:8280/services/ComponentsDbRest/component'
    for component_id in ids:
        with urllib.request.urlopen(f'{base_url}/{component_id}/data') as url:
            data = json.loads(url.read().decode())
        with open(f'divertor/{component_id}.json', 'w') as f:
            f.write(json.dumps(data))


if __name__ == '__main__':
    saveDivertorJson()

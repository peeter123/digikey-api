##########################
# Configuration logic
##########################

import os
import pickle
import time
from kicost_digikey_api_v3 import DK_API

class QueryCache(object):
    ''' Components queries cache implementation '''
    def __init__(self, path, ttl):
        self.path = path
        self.ttl_min = ttl*24*60
        self.suffix = ''

    def get_name(self, prefix, name):
        return os.path.join(self.path, prefix + '_' + name.replace('/', '_') + self.suffix + ".dat")

    def save_results(self, prefix, name, results):
        ''' Saves the results to the cache '''
        with open(self.get_name(prefix, name), "wb") as fh:
            pickle.dump(results, fh, protocol=2)

    def load_results(self, prefix, name):
        ''' Loads the results from the cache, must be implemented by KiCost '''
        file = self.get_name(prefix, name)
        print('Looking in cache '+file)
        if not os.path.isfile(file):
            return None, False
        mtime = os.path.getmtime(file)
        ctime = time.time()
        dif_minutes = int((ctime-mtime)/60)
        if self.ttl_min < 0 or (self.ttl_min > 0 and dif_minutes <= self.ttl_min):
            with open(file, "rb") as fh:
                result = pickle.loads(fh.read())
            print('Found in cache '+str(result))
            return result, True
        # Cache expired
        return None, False


def configure(cfg_file):
    if cfg_file is None:
        cfg_file = '~/.config/kicost_digikey_api_v3/config.txt'
    cfg_file = os.path.expanduser(cfg_file)
    cache = QueryCache('/tmp', 7)
    with open(cfg_file, 'rt') as f:
        for ln in f:
            if not ln.strip():
                continue
            val = ln.split('=')
            if len(val) != 2:
                print(f'Malformed {ln}')
                exit(1)
            key = val[0].strip()
            value =val[1].strip()
            if key == 'DIGIKEY_CLIENT_ID':
                DK_API.id = value
            elif key == 'DIGIKEY_CLIENT_SECRET':
                DK_API.secret = value
            elif key == 'DIGIKEY_CLIENT_SANDBOX':
                DK_API.sandbox = value.lower() == 'true'
            elif key == 'DIGIKEY_STORAGE_PATH':
                cache.path = value
            else:
                print(f'Unknown config option {key}')
                exit(1)
    if 'DIGIKEY_CLIENT_ID' in os.environ:
        DK_API.id = os.environ['DIGIKEY_CLIENT_ID']
    if 'DIGIKEY_CLIENT_SECRET' in os.environ:
        DK_API.secret = os.environ['DIGIKEY_CLIENT_SECRET']
    if 'DIGIKEY_CLIENT_SANDBOX' in os.environ:
        DK_API.sandbox = os.environ['DIGIKEY_CLIENT_SANDBOX'].lower() == 'true'
    if 'DIGIKEY_STORAGE_PATH' in os.environ:
        cache.path = os.environ['DIGIKEY_STORAGE_PATH']
    DK_API.configure(cache)
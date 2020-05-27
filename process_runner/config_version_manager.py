import json
from io import TextIOWrapper
from typing import Union

LATEST_VERSION = "1.0.0"

def file_to_dict(filename: str) -> dict:
    ''' Returns '''
    with open(filename, 'r') as file:
        cfg = json.load(file)

    return cfg

def new_config() -> dict:
    ''' Returns a new config from latest version '''
    
    return update_version({})

def is_latest(cfg):
    ''' Returns True of False if config dict is latest version format 

        Tests

        Test 1
        >>> foo = {}
        >>> is_latest(foo)
        False

        Test2
        >>> foo = {'version': '1.0.0'}
        >>> is_latest(foo)
        True
    '''

    # if cfg is a filename, return dict of opened file
    dct = file_to_dict(cfg) if isinstance(cfg, str) else cfg

    # returns true if version key is found and value is equal to latest version
    return 'version' in dct and dct['version'] == LATEST_VERSION
    
def update_version(config: Union[str, TextIOWrapper]):

    cfg_dict = {}
    
    if isinstance(config, str):
        with open(config, 'r') as file:
            cfg_dict = json.load(file.read())
    elif isinstance(config, dict):
        cfg_dict = config
    else:
        raise InvalidConfigParameter()

    latest_version(cfg_dict)
    return cfg_dict

def latest_version(cfg):
    return v1(cfg)

def v1(cfg):
    if 'version' not in cfg:
        cfg['version'] = '1.0.0'
    elif cfg['version'] != '1.0.0':
        cfg['version'] = '1.0.0'

    if 'host' not in cfg:
        cfg['cfg'] = '0.0.0.0'

    if 'port' not in cfg:
        cfg['port'] = 8010
    if 'program' not in cfg:
        cfg['program'] = ['echo', 'Howdy!']

    return cfg


class InvalidConfigParameter(Exception):

    def __init__(self, message='Unknown argument for manage version'):
        self.message = message
        super().__init__(self.message)

if __name__ in '__main__':
    import doctest
    doctest.testmod()
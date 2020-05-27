import json

def test():
    print('Test')

def manage_version(config):

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


class InvalidConfigParameter(Exception):

    def __init__(self, message='Unknown argument for manage version'):
        self.message = message
        super().__init__(self.message)
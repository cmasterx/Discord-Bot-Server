import os
import subprocess
import json
from secrets import token_urlsafe
from flask import Flask, jsonify, request
from flask_cors import CORS

import config_version_manager as cvm

app = Flask(__name__)
CORS(app)

config = None
token = None

try:
    file = open('config.json', 'r')
    config = json.loads(file.read())
    file.close()
    print('Loaded config file')


    
except OSError as err:
    print("Unable to find config.json. Setting config as empty")
    config = cvm.new_config()

    with open('config.json', 'w+') as file:
        json.dump(config, file)

except Exception as err:
    print(err)
    exit()

# todo start only program in config file
@app.route('/api/<string:token>/start/', methods=['GET', 'POST'])
def api_start(token):
    if request.method == 'POST':
        content = request.get_json()
        
        # todo fix
        if 'program' in content and content['program'] in config['program']:
            command = ['screen'] + content['program'] + ['&']
            subprocess.Popen(command)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        # if 'program' not in request.

    return jsonify({'invalid': False})

if __name__ in '__main__':
    host = config['host'] if 'host' in config else '0.0.0.0'
    port = config['port'] if 'port' in config and isinstance(config['port'], int) else 8010

    if 'token' in config:
        token = config['token']
    else:
        token = token_urlsafe(32)
        config['token'] = token

    # update config file
    # todo only save file if config in memory is different from file
    with open('config.json', 'w') as file:
        json.dump(config, file)
    
    app.run(host=host, port=port)

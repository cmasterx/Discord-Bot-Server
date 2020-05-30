import os
import subprocess
import json
import psutil
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
@app.route('/api/<string:_token>/start', methods=['GET', 'POST'])
def api_start(_token):
    
    if _token != token:
        print("Invalid token!")
        return jsonify({'valid': False, 'message': 'Invalid Token'})
    
    print("This is the stuff: ")
    if request.method == 'POST':
        content = request.get_json()
        print("This is the stuff: ")
        print(content)
        
        # todo fix
        if 'program' in content and content['program'] in config['program']:
            command = ['screen'] + content['program']
            subprocess.Popen(command)
            return jsonify({'success': True, 'ip': "mc.cmasterx.com"})
        else:
            return jsonify({'success': False})
        # if 'program' not in request.

    return jsonify({'valid': False})

@app.route('/api/<string:_token>/running', methods=['GET'])
def api_running(_token):

    if _token != token:
        return jsonify({'valid': False, 'message': 'Invalid Token'})

    if request.method == 'GET':
        if 'program' in request.args and request.args['program'] in config['runners']:
            program = request.args['program']

            for proc in psutil.process_iter():
                if proc.name() == program:
                    return jsonify({'valid': True, 'found': True})

            else:
                return jsonify({'valid': True, 'found': False})
        else:
            return jsonify({'valid': False, 'message': 'Cannot process GET request. \
                Either program is not a valid entry or no valid key in  URL'})

            # check if program name is in list of programs


    return jsonify({'valid': False, 'message': 'Unknown request'})

@app.route('/api/<string:_token>/stop', methods=['GET'])
def api_stop(_token):
    if _token != token:
        return jsonify({'valid': False, 'message': 'Invalid Token'})

    if request.method == 'GET':
        program_name = request.args['program']

        if 'program' in request.args and program_name in config['stop']:
            for proc in psutil.process_iter():
                if proc.name() == program_name:
                    proc.kill()
                    return jsonify({'valid': True, 'killed': True})
            
            return jsonify({'valid': True, 'killed': False})

        return jsonify({'valid': False, 'killed': False})
            
    else:
        return jsonify({'valid': False, 'message': 'Unknown request'})


if __name__ in '__main__':
    host = config['host'] if 'host' in config else '0.0.0.0'
    port = config['port'] if 'port' in config and isinstance(config['port'], int) else 8010

    if 'token' in config:
        token = config['token']
    else:
        token = token_urlsafe(32)
        config['token'] = token

    # build config file from missing parameters
    param_list = ['program', 'runners', 'stop']
    for element in param_list:
        if element not in config:
            config[element] = []

    # update config file
    # todo only save file if config in memory is different from file
    with open('config.json', 'w') as file:
        json.dump(config, file)
    
    app.run(host=host, port=port)

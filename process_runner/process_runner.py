import os
import subprocess
import json
from secrets import token_urlsafe
from flask import Flask, jsonify, request
from flask_cors import CORS

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
    config = {
        'host': '0.0.0.0',
        'port': 8010,
        'processname': 'program'
    }

    with open('config.json', 'w+') as file:
        json.dump(config, file)
except Exception as err:
    print(err)
    exit()


if __name__ in '__main__':
    host = config['host'] if 'host' in config else '0.0.0.0'
    port = config['port'] if 'port' in config and isinstance(config['port'], int) else 8010

    if 'token' in config:
        token = config['token']
    else:
        token = token_urlsafe(32)

    # update config file
    with open('config.json', 'w') as file:
        json.dump(config, file)
    
    app.run(host='0.0.0.0', port=8010)

import os
import json
import psutil
import subprocess
from subprocess import call
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/start/<string:progname>', methods=['GET'])
def start(progname):
    command = ['screen', './{}'.format(progname), '&']
    print(progname)
    subprocess.Popen(command)
    return "Program called"

@app.route('/stop/<string:progname>', methods=['GET'])
def end(progname):
    for proc in psutil.process_iter():
        print(proc.name())
        print(progname)
        if proc.name() == progname:
            print('here')
            proc.kill()
            return 'Killed program'

    return 'Failed to kill'

@app.route('/running/<string:progname>', methods=['GET'])
def is_running(progname):
    for proc in psutil.process_iter():
        if proc.name() == progname:
            return 'Found'

    return 'Not found'

if __name__ in '__main__':
    app.run(host='0.0.0.0', port=8000)
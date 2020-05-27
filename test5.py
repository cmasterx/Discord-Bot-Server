import subprocess
import time

command = ['screen', './program']
subprocess.Popen(command)

while True:
    time.sleep(1)
    print('Loop!')

# Calling a program in python
from subprocess import call

command = ['screen', './program']
call(command, shell=False)

# Calling a program in python
from subprocess import call

command = ['screen', '-r', './program']
call(command, shell=False)

import psutil

PROCNAME = "program"

for proc in psutil.process_iter():
    
    print("Found {}".format(proc.name()))
    
    if proc.name() == PROCNAME:
        print("Program found, killing")
        proc.kill()
#Timer in python
from time import sleep

def Timer():
    time = 0
    while time >= 0:
        time += 1
        sleep(1)
        return str(time)

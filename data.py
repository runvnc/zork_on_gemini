import os, subprocess, sys
from urllib.parse import unquote
from shlex import quote
from pathlib import Path
import time

parent_pipes = {}
child_pipes = {}

mypath = os.path.dirname(os.path.realpath(__file__))

def fname(which,usr): return f'{mypath}/data/{which}_{usr}'

def outf(usr): return fname('OUTPUT',usr)

def inpf(usr): return fname('INPUT', usr)

def activef(usr): return fname('ACTIVE', usr)

def user_active(usr): return os.path.exists(activef(usr))
    
def send_command(usr, cmd):
    with open(inpf(usr), 'w') as f:
        f.write(cmd)

def wait(usr, which, maxtries):
    time.sleep(0.25)
    tries = 0
    while tries < maxtries and not os.path.exists(which):
        time.sleep(0.25)
        print(__name__,which,"Waiting for file to exist:",which)
        tries += 1

def wait_for_output(usr):
    wait(usr, outf(usr), 100)
    with open(outf(usr)) as f:
        text = f.read()
    return text

def wait_for_input(usr):
    wait(usr, inpf(usr), 10)
    return os.path.exists(inpf(usr))

def wipe_all():
    for f in Path(f'{mypath}/data').glob('*'):
        if f.is_file(): f.unlink()

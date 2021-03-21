import os, subprocess, sys
from urllib.parse import unquote
from shlex import quote
from pathlib import Path
import time
from multiprocessing import Process, Pipe, set_start_method
import logging

#parent_pipes = {}
#child_pipes = {}

mypath = os.path.dirname(os.path.realpath(__file__))

def spawn_session(usr, func):
    user = usr
    set_start_method('spawn')
    #parent_conn, child_conn = Pipe()
    #parent_pipes[user] = parent_conn
    #child_pipes[user] = child_conn
    p = Process(target=func, args=(user,))
    p.daemon = True
    p.start()

def checkpipe(usr, direction):
    if not os.path.exists(f'{mypath}/data/app_{direction}_{usr}'):
        Path(f'{mypath}/data/app_{direction}_{usr}').touch()
        return False
    else:
        return True

def writepipe(usr, direction,data):
    checkpipe(usr, direction)
    logging.info(f"attempt to open write to pipe {usr} {direction}")
    with open(f"{mypath}/data/app_{direction}_{usr}",'w') as f:
        f.write(data)
    logging.info(f"wrote data to {direction}: "+data)
        
def readpipe(usr, direction):
    checkpipe(usr, direction)
    logging.info(f"attempt to open read from pipe {usr} {direction}")
    text = ''
    with open(f'{mypath}/data/app_{direction}_{usr}','r') as f:
        logging.info(f"attempt to read from pipe {usr} {direction}")
        text = f.read()
        logging.info(f"read complete {usr} {direction}")
    os.remove(f'{mypath}/data/app_{direction}_{usr}')
    return text
    
def waitread(usr, direction):
    txt = ''
    tries = 0
    while tries < 44 and txt == '':
        txt = readpipe(usr,direction)
        time.sleep(0.35)
        tries += 1
    return txt
   
def user_active(usr):
    return checkpipe(usr,'active')
    


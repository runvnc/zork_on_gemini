#!/usr/bin/python3
import os, subprocess, sys
from urllib.parse import unquote
from shlex import quote
from pathlib import Path
import time

mypath = os.path.dirname(os.path.realpath(__file__))

query = unquote(os.environ["QUERY_STRING"])
user = ''
if 'REMOTE_USER' in os.environ:
    user = unquote(os.environ["REMOTE_USER"])

def user_active(usr):
    return os.path.exists('ACTIVE_'+usr)
    
def spawn_session(usr):
    subprocess.Popen([mypath+'/control_zork.py',quote(usr)],close_fds=True,creation_flags=8)
    Path(mypath+'/ACTIVE_'+usr).touch()

def send_command(usr, cmd):
    with open(mypath+'/INPUT_'+usr, 'w') as f:
        f.write(cmd)

def wait_for_zork(usr):
    time.sleep(0.25)
    tries = 0
    while tries < 100 and not os.path.exists(mypath+'/OUTPUT_'+usr):
        time.sleep(0.25)
        tries += 1
    with open(mypath+'/OUTPUT_'+usr) as f:
        text = f.read()    
    return text
        
if user != '':
    if query == "__INPUT__":
        print("10 >\r\n")
    else:
        print("20 text/gemini\r\n")
        print(f'Logged in as [{user}]')

        print("```shell")

        if user_active(user):
            send_command(user, query)
            text = wait_for_zork(user)
            print(text)
        else:
            spawn_session(user)     
            text = wait_for_zork(user)
            print(text)
                    
        print("\r\n```")
        print("=> zork.cgi?__INPUT__ >")
else:
    print("60 Client certificate required to identify session.\r\n")

#!/usr/bin/python3
import os, subprocess, sys
from urllib.parse import unquote
from shlex import quote
from pathlib import Path
import time
from data import *
from gemini import *
    
def spawn_session(usr):
    subprocess.Popen([mypath+'/control_zork.py',quote(usr)],
                     shell=True,stdin=subprocess.PIPE)
    Path(activef(usr)).touch()

if user != '':
    if query == "__INPUT__":
        respond(INPUT, '>')
    else:
        respond(SUCCESS, 'text/gemini')
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
        print("=> zork.cgi?__INPUT__ < Click to input Zork command >")
else:
    respond(NEED_CERT, 'Client certificate required to log in.')

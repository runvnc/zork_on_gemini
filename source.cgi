#!/usr/bin/python3
import os, subprocess, sys, time, traceback, logging
from urllib.parse import unquote
from pathlib import Path
from data_redis import *
from gemini import *
from control_zork import *

def show(fname):
    with open(fname,'r') as f:
        print(f'## {fname}')
        print('```python')
        for line in f:
            if not line.lstrip().startswith("#") and \
               not line.lstrip().startswith("logging"):
                print(line.replace("\n",""))
        print('```')

respond(SUCCESS, 'text/gemini')
print("# Source code")
print()
print("Note: on this page the comments (which are actually just dead code) and logging are stripped out to make it easier to understand. Also note, I have not written a lot of Python code before.")
show('zork.cgi')
show('control_zork.py')
show('data_redis.py')
show('spawner.py')
print()
print("=> https://github.com/runvnc/zork_on_gemini/ Full source on github")

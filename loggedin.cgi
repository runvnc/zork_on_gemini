#!/usr/bin/python
import os, subprocess, sys, time, traceback, logging
from urllib.parse import unquote
from pathlib import Path
from data_redis import *
from gemini import *
from control_zork import *

respond(SUCCESS, 'text/gemini')


loggedin=subprocess.check_output("ps aux|grep zork|awk '{print $NF}'",shell=True).decode()
list = loggedin.split()
count = 0
str = ''
for item in list:
    if item != 'zork' and ("$NF" not in item) and (".pem" not in item):
        if count > 0: str += ", "
        count += 1
        str += item
print(f"Total logged in: {count}")
print()   
print(str)

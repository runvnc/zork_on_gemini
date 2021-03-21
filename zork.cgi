#!/usr/bin/python3
import os, subprocess, sys, time, traceback, logging
from urllib.parse import unquote
from pathlib import Path
from data_redis import *
from gemini import *
from control_zork import *

logging.basicConfig(filename='zorkcgi.log', level=logging.DEBUG)
logging.info('--------------------------------------------------------------')

if __name__ == '__main__':
    if user != '':
        if query == "cmd":
            respond(INPUT, '>')
        else:
            respond(SUCCESS, 'text/gemini')
            print(f'Logged in as [{user}]')

            print("```shell")
            try:
                if user_active(user):
                    logging.info(f"{user} is active! sending {query}")
                    writepipe(user,'down',query)
                    #time.sleep(0.5)
                    text = waitread(user,'up')
                    print(text)
                else:
                    logging.info(f'{user} is not active, spawning')
                    checkpipe(user,'up',True)
                    spawn_session(user, init)
                    #time.sleep(0.2)
                    logging.info('parent trying to receive from child')
                    text = waitread(user,'up')
                    logging.info("parent got the output")
                    print(text)
                            
                print("\r\n```")
                print("=> zork.cgi?cmd < Input Zork command >")
            except Exception as err:
                print("Error:")
                print(err)
                t, v, trace = sys.exc_info()
                print(t,v)
                print(trace.format_exc)
    else:
        respond(NEED_CERT, 'Client certificate required to log in.')

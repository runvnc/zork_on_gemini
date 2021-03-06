#!/usr/bin/python
import os, subprocess, sys, time, traceback, logging
from urllib.parse import unquote
from pathlib import Path
from data_redis import *
from gemini import *
from control_zork import *

logging.basicConfig(filename='zorkcgi.log', level=logging.DEBUG)
logging.info('--------------------------------------------------------------')

def esc_markdown(s):
    if s is None: return ''
    escaped = s.translate(
        str.maketrans({"]":  r"\]","\\": r"\\","#": r"\#",
                       ">": r"\>", "^":  r"\^",  "$":  r"\$",
                       "*":  r"\*"}))
    return escaped

if __name__ == '__main__':
    if user != '':
        if query == "cmd":
            respond(INPUT, '>')
        else:
            respond(SUCCESS, 'text/gemini')
            print("# Zork")
            print(f'## [{user}]')
            print()
            #print("```shell")
            try:
                if user_active(user):
                    logging.info(f"{user} is active! sending {query}")
                    writepipe(user,'down',query)
                    #time.sleep(0.5)
                    text = waitread(user,'up')
                    print(esc_markdown(text))
                else:
                    logging.info(f'{user} is not active, spawning')
                    checkpipe(user,'up',True)
                    spawn_session(user, init)
                    time.sleep(0.25)
                    logging.info('parent trying to receive from child')
                    text = waitread(user,'up')
                    logging.info("parent got the output")
                    print(esc_markdown(text))
                            
                #print("\r\n```")
                print()
                print("=> zork.cgi?cmd â¨ī¸  Input command")
                print("=> zork.cgi?look đ Look")
                print("=> zork.cgi?help â Help")
                print("=> zork.cgi?info âšī¸ Info")
                print("=> zork.cgi?inventory đ Inventory")
                print("=> zork.cgi?save đž Save")
                print("=> zork.cgi?restore đ Restore")
                print(f"=> {user}.dat đĨ Download save file")

            except Exception as err:
                print("Error:")
                print(err)
                t, v, trace = sys.exc_info()
                print(t,v)
                print(trace.format_exc)
    else:
        respond(NEED_CERT, 'Client certificate required to log in.')

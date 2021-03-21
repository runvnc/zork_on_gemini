import os, subprocess, sys
from urllib.parse import unquote
from pathlib import Path
import time
from multiprocessing import Process, set_start_method
import logging, redis, datetime

pubsub = {}

mypath = os.path.dirname(os.path.realpath(__file__))
redisconn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def spawn_session(usr, func):
    redisconn.publish('app_spawn',usr)
#    user = usr
#    logging.info("Trying to spawn")
#    set_start_method('spawn')
#    p = Process(target=func, args=(user,))
#    p.daemon = True
#    p.start()
#    logging.info("Spawned?")
#    redisconn.set(f'active_{usr}', 1)
#    logging.info("Set active")

def checkpipe(user, direction, sub=False):
    key = f'app_{direction}_{user}'
    if key in pubsub:
        return pubsub[key]
    else:
        pubsub[key] = redisconn.pubsub()
        if sub:
            logging.info(f"Subscribing to app_{direction}_{user}")
            pubsub[key].subscribe(f'app_{direction}_{user}')
        return pubsub[key]
        
def writepipe(usr, direction,data):
    logging.info(f"Trying to publish app_{direction}_{usr} :" + data)
    redisconn.publish(f'app_{direction}_{usr}',data)
        
def readpipe(usr, direction):
    pipe = checkpipe(usr,direction,True)
    msg = pipe.get_message()
    logging.info(__name__+"msg from sub is "+str(msg))
    if not (msg is None) and msg['type'] == 'subscribe':
        msg = pipe.get_message()
    if msg is None: return None
    logging.info("pipe received message: "+str(msg))
    return msg['data']
    
def waitread(usr, direction):
    txt = None
    tries = 0
    while tries < 30 and txt == None:
        txt = readpipe(usr,direction)
        if not not (txt is None):
            read = ''
            while not (read is None):
                read = readpipe(usr,direction)
                if not (read is None): txt += "\r\n" + read
        time.sleep(0.05)
        tries += 1
    return txt
   
def user_active(usr):
    return redisconn.exists(f'active_{usr}')
    


#!/usr/bin/python
import os, subprocess, sys
from urllib.parse import unquote
from pathlib import Path
import time
from multiprocessing import Process, set_start_method
import logging, redis, datetime
from control_zork import *

logging.basicConfig(filename='zorkspawner.log', level=logging.CRITICAL)

pubsub = {}

mypath = os.path.dirname(os.path.realpath(__file__))
redisconn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = redisconn.pubsub()
pubsub.subscribe('app_spawn')

def checkmessages():
    while True:
        for msg in pubsub.listen():
            if msg != None and msg['type'] != 'subscribe':
                spawn_session(msg['data'], init)
            time.sleep(0.1)

def spawn_session(usr, func):
    user = usr
    logging.info("Trying to spawn")
    p = Process(target=func, args=(user,))
    p.daemon = True
    p.start()
    logging.info("Spawned?")
    redisconn.set(f'active_{usr}', 1)
    logging.info("Set active")

checkmessages()

#!/usr/bin/python3
import os, pexpect, sys, time, traceback
from data_redis import *
import logging
import pexpect.replwrap
import atexit

logging.basicConfig(filename='zorkspawner.log', level=logging.DEBUG)

def exiting():
    logging.info("Child  exiting for some reason."+__name__)

def init(user):
    if os.fork() == 0:  # <--
        return 
    atexit.register(exiting) 
    logging.info("Child Spawning Zork..")
    #child = pexpect.spawn(mypath+'/zork',encoding='utf-8')
    child = pexpect.replwrap.REPLWrapper(mypath+'/zork',"\n>",None)
    #child.logfile = open(mypath+'/outzork.log','w')
    logging.info("Child Waiting for prompt..")
    text = child.run_command('look')
    logging.info("Child sending Zork initial output..")
    writepipe(user,'up',text)
    logging.info("Child start of loop")
    #logging.info("child status:" + str(child.status))
    while True:
        try:
            logging.info("Child Trying to receive..")
            redisconn.set(f'ping_{user}',time.time())
            cmd = waitread(user,'down')
            #print("Child sending to zork: "+str(cmd))
            if not (cmd is None):
                if cmd != '' and cmd != ' ':
                    text = child.run_command(cmd)
                #print("Child done with sendline to zork: "+cmd)
                #print("received result: ",text)
            else:
                logging.info("Child read none!")
            writepipe(user,'up',text)
        except Exception as e:
            logging.info("Exception in control_zork!")
            logging.info(traceback.format_exception(*sys.exc_info()))
            
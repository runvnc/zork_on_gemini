#!/usr/bin/python
import os, pexpect, sys, time, traceback
from data_redis import *
import logging
import pexpect.replwrap
import atexit

APPTIMEOUT = 60 * 30
PINGINTERVAL = 1

def exiting():
    logging.info("Child  exiting for some reason."+__name__)

def init(user):
    if os.fork() == 0:  # <--
        return 
    logging.basicConfig(filename='spawner.log', level=logging.DEBUG)

    lastinput = time.time()
    lastping = time.time()
    atexit.register(exiting) 
    logging.info("Child Spawning Zork..")
    #child = pexpect.spawn(mypath+'/zork',encoding='utf-8')
    torun = mypath+f'/zork {user}'
    prompt = "\n>"
    child = pexpect.replwrap.REPLWrapper(torun,prompt,None)
    #child.logfile = open(mypath+'/outzork.log','w')
    logging.info("Child Waiting for prompt..")
    text = child.run_command('look')
    logging.info("Child sending Zork initial output..")
    writepipe(user,'up',text)
    logging.info("Child start of loop")
    #logging.info("child status:" + str(child.status))
    while True:
        try:
            if time.time()-lastinput>APPTIMEOUT:
                logging.info("Timeout. Suicide.")
                sys.exit(0)
            if time.time()-lastping>PINGINTERVAL:
                logging.info("Child Trying to receive..")
                redisconn.set(f'ping_{user}',time.time())
                lastping = time.time()
            cmd = waitread(user,'down')
            #print("Child sending to zork: "+str(cmd))
            if not (cmd is None):
                if cmd != '' and cmd != ' ':
                    lastinput = time.time()
                    try:
                        text = child.run_command(cmd,timeout=0.15)
                    except Exception as ee:
                        text = child.child.before
                        if not child.child.isalive():
                            text = child.child.before
                            writepipe(user,'up',text)
                            logging.info("App ended. Exiting.")
                            sys.exit(0)                       
                    writepipe(user,'up',text)
                #print("Child done with sendline to zork: "+cmd)
                #print("received result: ",text)
            #else:
            #    logging.info("Child read none!")
            
        except Exception as e:
            logging.info("Exception in control_zork!")
            logging.info(traceback.format_exception(*sys.exc_info()))
            

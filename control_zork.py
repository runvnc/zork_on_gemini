#!/usr/bin/python3
import os, pexpect, sys, time

mypath = os.path.dirname(os.path.realpath(__file__))

user = sys.argv[1]

child = pexpect.spawn(mypath+'/zork',encoding='utf-8')
child.logfile = open(mypath + "/OUTPUT_" + user,'w')
child.expect(">")

def wait_for_input():
    tries = 0
    time.sleep(0.25)
    while tries < 10 and not os.path.exists(mypath+'/INPUT_'+user):
        time.sleep(0.25)
        tries += 1
    return os.path.exists(mypath+'/INPUT_'+user)

while True:
    if wait_for_input():
        with open(mypath+'/INPUT_'+user) as f:
            cmd = f.read()
        os.remove(mypath+'/INPUT_'+user)
        child.sendline(cmd)
        child.expect(">")

#!/usr/bin/python3
import os, pexpect, sys, time
from data import *

user = sys.argv[1]

child = pexpect.spawn(mypath+'/zork',encoding='utf-8')
child.logfile = open(outf(user),'w')
child.expect(">")

while True:
    if wait_for_input():
        with open(inpf(user)) as f:
            cmd = f.read()
        os.remove(inpf(user))
        child.sendline(cmd)
        child.expect(">")

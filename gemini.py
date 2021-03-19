import os
from urllib.parse import unquote
from shlex import quote
from pathlib import Path

query = unquote(os.environ["QUERY_STRING"])
user = ''
if 'REMOTE_USER' in os.environ:
    user = unquote(os.environ["REMOTE_USER"])

def respond(code, meta): 
	print(f'{code} {meta}\r\n')

INPUT = 10
NEED_CERT = 60
SUCCESS = 20
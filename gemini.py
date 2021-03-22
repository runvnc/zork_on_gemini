import os
from urllib.parse import unquote
from shlex import quote
from pathlib import Path

query = unquote(os.environ["QUERY_STRING"])
user = ''
if 'REMOTE_USER' in os.environ:
    user = quote(unquote(os.environ["REMOTE_USER"]))
    user = user[:30]
    user += '_'+unquote(os.environ["TLS_CLIENT_HASH"])[-5:]

def respond(code, meta): 
	print(f'{code} {meta}\r\n')

INPUT = 10
NEED_CERT = 60
SUCCESS = 20
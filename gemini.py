import os
from urllib.parse import unquote
from shlex import quote
from pathlib import Path
import shortuuid

query = ''
if 'QUERY_STRING' in os.environ:
    query = unquote(os.environ["QUERY_STRING"])
user = ''
if 'REMOTE_USER' in os.environ:
    user = quote(unquote(os.environ["REMOTE_USER"]))
    user = user[:30]
    if 'TLS_CLIENT_HASH' in os.environ:
        user += '_'+unquote(os.environ["TLS_CLIENT_HASH"])[-5:]
    else:
        user += '_'+shortuuid.uuid()[-5:]

def respond(code, meta): 
	print(f'{code} {meta}\r\n')

INPUT = 10
NEED_CERT = 60
SUCCESS = 20

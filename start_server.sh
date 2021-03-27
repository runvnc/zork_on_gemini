#!/bin/bash
rm *.log
redis-cli --scan --pattern active* | xargs redis-cli del

while true; do
    jetforce --hostname zork.club --host 167.71.119.170  --tls-certfile /etc/letsencrypt/live/zork.club/fullchain.pem --tls-keyfile /etc/letsencrypt/live/zork.club/privkey.pem 
done

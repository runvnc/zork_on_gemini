#!/bin/bash
rm -rf data/*
rm *.log
redis-cli --scan --pattern active* | xargs redis-cli del
jetforce

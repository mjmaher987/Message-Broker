#!/bin/bash
# Order test

BASE_DIR=$(git rev-parse --show-toplevel)/message-broker-server

rm -r $BASE_DIR/server/8000
rm -r $BASE_DIR/server/8001

rm client.log
rm server_8000.log
rm server_8001.log

pkill -9 python

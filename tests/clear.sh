#!/bin/bash
# Order test

BASE_DIR=$(git rev-parse --show-toplevel)/message-broker-server

rm -r $BASE_DIR/server/8000

pkill -9 python

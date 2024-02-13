#!/bin/bash

BASE_DIR=$(git rev-parse --show-toplevel)/message-broker-server

SETTING_PORT=8001
export SETTING_PORT=$SETTING_PORT
mkdir $BASE_DIR/server/$SETTING_PORT
cp $BASE_DIR/server/server/settings.py $BASE_DIR/server/$SETTING_PORT/settings.py
python $BASE_DIR/server/manage.py migrate --settings=$SETTING_PORT.settings
python $BASE_DIR/server/manage.py runserver 0.0.0.0:$SETTING_PORT --settings=$SETTING_PORT.settings &
sleep 5
python $BASE_DIR/server/connect.py &
sleep 2
echo $SETTING_PORT 'Connected!'
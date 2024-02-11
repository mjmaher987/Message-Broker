#!/bin/bash
# Test for handling 3 nodes

BASE_DIR=$(git rev-parse --show-toplevel)/message-broker-server

python $BASE_DIR/coordinator/manage.py flush --noinput
python $BASE_DIR/coordinator/manage.py migrate
python $BASE_DIR/coordinator/manage.py runserver 0.0.0.0:7000 &
sleep 5
echo 'Coordinator Connected!'

SETTING_PORT=8000
export SETTING_PORT=$SETTING_PORT
mkdir $BASE_DIR/server/$SETTING_PORT
cp $BASE_DIR/server/server/settings.py $BASE_DIR/server/$SETTING_PORT/settings.py
python $BASE_DIR/server/manage.py migrate --settings=$SETTING_PORT.settings
python $BASE_DIR/server/manage.py runserver 0.0.0.0:$SETTING_PORT --settings=$SETTING_PORT.settings &
sleep 5
python $BASE_DIR/server/connect.py &
sleep 2
echo $SETTING_PORT 'Connected!'

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

SETTING_PORT=8002
export SETTING_PORT=$SETTING_PORT
mkdir $BASE_DIR/server/$SETTING_PORT
cp $BASE_DIR/server/server/settings.py $BASE_DIR/server/$SETTING_PORT/settings.py
python $BASE_DIR/server/manage.py migrate --settings=$SETTING_PORT.settings
python $BASE_DIR/server/manage.py runserver 0.0.0.0:$SETTING_PORT --settings=$SETTING_PORT.settings &
sleep 5
python $BASE_DIR/server/connect.py &
sleep 2
echo $SETTING_PORT 'Connected!'

python $BASE_DIR/tests/2/test.py

rm -r $BASE_DIR/server/8000
rm -r $BASE_DIR/server/8001
rm -r $BASE_DIR/server/8002

pkill -9 python

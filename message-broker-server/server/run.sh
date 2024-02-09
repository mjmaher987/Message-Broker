#!/bin/bash

python manage.py runserver 0.0.0.0:8000 &
sleep 5
python connect.py --coordinator_ip "192.168.117.69"
echo 'Connected!'
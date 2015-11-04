#!/bin/bash

install -m 755 /home/source/rc.local /etc

pip install bottle
pip install youtube-dl
ln -s /usr/local/bin/youtube-dl /usr/bin/

mkdir -m 755 -p /opt/youtube
# install -m 755 /home/source/app/main.py /opt/youtube
cp -r /home/source/app/* /opt/youtube

exit 0

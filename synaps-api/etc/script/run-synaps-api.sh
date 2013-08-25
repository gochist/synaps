#!/bin/bash

# clean up
sudo rm -rf /opt/stack/synaps/synaps-api/build
sudo rm -rf /opt/stack/synaps/synaps-api/dist

# build synaps
cd /opt/stack/synaps/synaps-api && sudo python setup.py sdist
cp /opt/stack/synaps/synaps-api/dist/*.tar.gz /opt/stack/synapsdist

# deploy synaps
cd /opt/stack/synapsdist
SYNAPSAPI=`ls -lrt synaps*tar.gz | tail -n1 | awk '{print $9}'i`
sudo pip install -U $SYNAPSAPI
sudo chmod 755 /etc/init.d/synaps* 
sudo chmod 755 /etc/init.d/storm*
sudo service synaps-api restart


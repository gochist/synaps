#!/bin/bash

# start infra service
sudo service rabbitmq-server restart
sudo service cassandra restart
sudo service zkServer.sh restart
cd /opt/storm/
sudo rm -rf /opt/storm/storm-local
nohup /opt/storm/bin/storm nimbus & > /dev/null
nohup /opt/storm/bin/storm ui & > /dev/null
sleep 10
nohup /opt/storm/bin/storm supervisor & > /dev/null

/home/june/bin/run-synaps-api.sh
/home/june/bin/run-synaps-storm.sh


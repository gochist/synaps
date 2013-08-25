#!/bin/bash

export JAVA_HOME=/usr/lib/jvm/java-6-openjdk-amd64
echo "Stop synaps topology"
/opt/storm/bin/storm kill synaps00 -w 5

rm -rf /opt/stack/synaps/synaps-storm/target
cd /opt/stack/synaps/synaps-storm && mvn clean && mvn package
cp /opt/stack/synaps/synaps-storm/target/*.jar /opt/stack/synapsdist
cd /opt/stack/synapsdist
SYNAPSSTORM=`ls -lrt synaps*jar | grep -v depen | tail -n1 | awk '{print $9}'`
rm storm-synaps.jar
ln -s $SYNAPSSTORM storm-synaps.jar

echo "Start synaps topology"
/opt/storm/bin/storm jar /opt/stack/synapsdist/storm-synaps.jar com.spcs.synaps.PutMetricTopology 00

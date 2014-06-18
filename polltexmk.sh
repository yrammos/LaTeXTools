#! /bin/bash
status=`cat ~/.lytexstat.log`
while [ "$status" == "RUNNING" ]; do
        sleep 1
        status=`cat ~/.lytexstat.log`
done
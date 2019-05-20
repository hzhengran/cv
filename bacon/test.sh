#!/bin/bash

touch totalTime.log

start=`date +"%s"`
echo "start-time:  $start" >> totalTime.log
for (( i=0; i<11; i++ ))
do
    {
       echo "multiprocess"
       aws s3 cp s3://bdm-workshop/informatica_1022_server_linux-x64.tar . --region cn-north-1 
       sleep 3
       # rm -rf info*
    } &  
done
wait    
end=`date +"%s"`
echo "end-time:  $end" >> totalTime.log
delta=`expr $end - $start`
echo "delta time:  $delta" >> totalTime.log

rm -rf info*

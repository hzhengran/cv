#!/bin/bash

FILE=a.log
touch $FILE

start=`date +"%s"`
echo "`date +%F` `date +%T`: Begin" >> $FILE
#for (( i=0; i<4; i++ ))
for i in $(seq 2) 
do
    {
       echo "multiprocess"
       aws s3 cp s3://bdm-workshop/informatica_1022_server_linux-x64.tar . --region cn-north-1 
       sleep 300
       # rm -rf info*
       wait
    } # &  
done
wait    
end=`date +"%s"`
echo "`date +%F` `date +%T`: End" >> $FILE
delta=`expr $end - $start`
echo "delta time:  $delta" >> $FILE

rm -rf info*

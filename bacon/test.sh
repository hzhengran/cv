#!/bin/bash

FILE=a.log
touch $FILE

start=`date +"%s"`
echo "`date +%F` `date +%T`: Begin" >> $FILE
for (( i=0; i<1; i++ ))
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
echo "`date +%F` `date +%T`: End" >> $FILE
delta=`expr $end - $start`
echo "delta time:  $delta" >> $FILE

rm -rf info*

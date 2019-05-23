#!/bin/bash

FILE=b.log
touch $FILE

start=`date +"%s"`
echo "`date +%F` `date +%T`: Begin" >> $FILE
for (( i=0; i<400; i++ ))
# for i in $(seq 2) 
do
    {
       echo "multiprocess"
       echo "`date +%F` `date +%T`: $i time begins" >> $FILE
       echo "`date +%F` `date +%T`: $i time completed" >> $FILE

       # sleep 300
       rm -rf info*
       echo "Deleted completed. $i" >> $FILE

       wait
    } # &  
done
wait    
end=`date +"%s"`
echo "`date +%F` `date +%T`: End" >> $FILE
delta=`expr $end - $start`
echo "delta time:  $delta" >> $FILE

rm -rf info*

#!/bin/bash
start=`date +"%s"`
for (( i=0; i<10; i++ ))
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
echo "time: " `expr $end - $start`

rm -rf info*

#!/bin/bash


# if filename not supplied at the command prompt
# use default file name
if [ $# -eq 0 ] 
then
   FILE=c.log
else
   FILE=$1
fi

touch $FILE

start=`date +"%s"`
echo "`date +%F` `date +%T`: Begin" >> $FILE

i=0
while : 
do
    {
       echo "multiprocess"
       let i++
       echo "`date +%F` `date +%T`: $i time begins" >> $FILE
       aws s3 cp s3://bdm-workshop/informatica_1022_server_linux-x64.tar . --region cn-north-1 
       echo "`date +%F` `date +%T`: $i time completed" >> $FILE

       # sleep 300
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

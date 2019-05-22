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
       task_start=`date +"%s"`
       aws s3 cp s3://bdm-workshop/informatica_1022_server_linux-x64.tar . --region cn-north-1 
       task_end=`date +"%s"`
       delta=`expr $task_end - $task_start`
       echo "task $i delta time:  $delta" >> $FILE
       echo "`date +%F` `date +%T`: $i time completed" >> $FILE
      
       sleep 30
       rm -rf info*
    }
done
  
end=`date +"%s"`
echo "`date +%F` `date +%T`: End" >> $FILE
delta=`expr $end - $start`
echo "delta time:  $delta" >> $FILE

rm -rf info*

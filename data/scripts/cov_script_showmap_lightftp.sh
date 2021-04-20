#!/bin/bash

folder=$1   #fuzzer result folder
pno=$2      #port number
step=$3     #step to skip running gcovr and outputting data to covfile
            #e.g., step=5 means we run gcovr after every 5 test cases
fmode=$4    #file mode -- structured or not
            #fmode = 0: the test case is a concatenated message sequence -- there is no message boundary
            #fmode = 1: the test case is a structured file keeping several request messages

#clear ftp data
#this is a LightFTP-specific step
#we need to clean the ftp shared folder to prevent underterministic behaviors.
ftpclean

#files stored in replayable-* folders are structured
#in such a way that messages are separated
if [ $fmode -eq "1" ]; then
  testdir="replayable-queue"
  replayer="aflnet-showmap"
else
  testdir="queue"
  replayer="aflnet-showmap"
fi

traceDir="trace_data"
abs_folder=$(readlink -f $folder)

#process initial seed corpus first
for f in $(echo $folder/$testdir/*.raw); do 

  #terminate running server(s)
  pkill fftp

  ftpclean  
  file_name=$(echo "$f" | awk -F/ '{print $(NF)}')
  trace_data=$(echo $abs_folder/$traceDir/$file_name)
  echo "proceeding.." $f

  $replayer -o $trace_data -f $f -s FTP -p $pno -q -e -- ./fftp fftp.conf $pno

done

#process fuzzer-generated testcases
count=0
for f in $(echo $folder/$testdir/id*); do 

  count=$(expr $count + 1)
  rem=$(expr $count % $step)
  if [ "$rem" != "0" ]; then continue; fi


  #terminate running server(s)
  pkill fftp
  
  ftpclean  
  file_name=$(echo "$f" | awk -F/ '{print $(NF)}')
  trace_data=$(echo $abs_folder/$traceDir/$file_name)
  echo "proceeding.." $f

  $replayer -o $trace_data -f $f -s FTP -p $pno -q -e -- ./fftp fftp.conf $pno

done
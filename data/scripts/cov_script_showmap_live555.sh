#!/bin/bash

folder=$1   #fuzzer result folder
pno=$2      #port number
step=$3     #step to skip running gcovr and outputting data to covfile
            #e.g., step=5 means we run gcovr after every 5 test cases
fmode=$4    #file mode -- structured or not
            #fmode = 0: the test case is a concatenated message sequence -- there is no message boundary
            #fmode = 1: the test case is a structured file keeping several request messages

# traceDir=$5

#clear gcov data

#output the header of the coverage file which is in the CSV format
#Time: timestamp, l_per/b_per and l_abs/b_abs: line/branch coverage in percentage and absolutate number

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
# abs_traceDir=$(readlink -f $traceDir)

# echo $abs_folder 
# echo $abs_traceDir

#process initial seed corpus first
for f in $(echo $abs_folder/$testdir/*.raw); do 

  #terminate running server(s)
  pkill testOnDemandR
  file_name=$(echo "$f" | awk -F/ '{print $(NF)}')
  trace_data=$(echo $abs_folder/$traceDir/$file_name)
  echo "proceeding.." $f
  $replayer -o $trace_data -f $f -s RTSP -p 8554 -q -e -- /home/setsal/project/sqlab/fuzzer/live555/testProgs/testOnDemandRTSPServer 8554  
  # wait
done


count=0
#process other testcases
for f in $(echo $folder/$testdir/id*); do 

  count=$(expr $count + 1)
  rem=$(expr $count % $step)
  if [ "$rem" != "0" ]; then continue; fi

  #terminate running server(s)
  pkill testOnDemandR

  file_name=$(echo "$f" | awk -F/ '{print $(NF)}')
  trace_data=$(echo $abs_folder/$traceDir/$file_name)
  echo "proceeding.." $f
  $replayer -o $trace_data -f $f -s RTSP -p 8554 -q -e -- /home/setsal/project/sqlab/fuzzer/live555/testProgs/testOnDemandRTSPServer 8554  

done
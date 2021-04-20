import os
import sys
import time
import matplotlib.pyplot as plt
import glob
import subprocess
from collections import Counter
import numpy as np

default_arg = "/home/setsal/project/sqlab/fuzzer/live555/testProgs/testOnDemandRTSPServer 8554"


def plotData(plt, data, t):
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    if(t == 0):
        plt.plot(x, y, '-', label='AFLNET')
    elif(t == 1):
        plt.plot(x, y, '-', label='AFLDEV')
    elif(t == 2):
        plt.plot(x, y, '-', label='kmeans-AFL')
    elif(t == 3):
        plt.plot(x, y, '-', label='original-Yuan-fuzz')
    elif(t == 4):
        plt.plot(x, y, '-', label='kmeans-Yuan-fuzz')


file_count = int(sys.argv[1])
data = []


for fc in range(file_count):
    # parse arg
    dirpath = sys.argv[2+fc]

    file_list = [os.path.basename(x)
                 for x in glob.glob(dirpath+"/trace_data/id*")]

    file_list.sort()

    time_array = []
    for f in file_list:
        mofidy_time = int(os.path.getmtime(dirpath+"/replayable-queue/" + f))
        time_array.append(mofidy_time)

    # all_data = []

    # for i in range(len(time_array)):
    #     all_data.append([file_list[i], time_array[i]])

    basetime = time_array[0]

    raw_bitmap = {}

    tmp_cnt = []
    trace_data_raw = ''
    for i in range(len(file_list)):
        argv = default_arg.split()

        trace_data_location = dirpath + '/trace_data/' + file_list[i]

        with open(trace_data_location, 'r') as f:
            trace_data_raw = f.read()

        tmp_list = []

        for line in trace_data_raw.splitlines():
            edge = line.split(':')[0]
            tmp_cnt.append(edge)
            tmp_list.append(edge)
        raw_bitmap[file_list[i]] = tmp_list

    counter = Counter(tmp_cnt).most_common()

    label = [int(f[0]) for f in counter]

    bitmap = np.zeros((len(file_list), len(label)))
    for idx, i in enumerate(file_list):
        tmp = raw_bitmap[i]
        for j in tmp:
            if int(j) in label:
                bitmap[idx][label.index(int(j))] = 1
    print(f"all edge = {len(label)}")
    basetime = time_array[0]
    # time
    time = 24 * 6
    plt_array = []
    for i in range(1, time + 1):
        block = np.zeros(len(label))
        for j in range(len(file_list)):
            if(time_array[j] < basetime + (i*60*10)):
                block = block + bitmap[j]
        count = 0
        for j in block:
            if j > 0:
                count = count + 1
        plt_array.append((i * 10, count))
        print(f"{(i * 10)} {count}")
    plotData(plt, plt_array, fc)

plt.title('Live555(RTSP)')
plt.ylabel('edge coverage')
plt.xlabel('time(minute)')
plt.legend(loc='best')
plt.show()
# print(len(time_array))
# basetime = time_array[0]
# end = time_array[-1]
# bound = int(((end - basetime)/600))+2

#     plt_array = []
#     for i in range(1, bound):
#         count = 0
#         for j in time_array:
#             if(j < (basetime + (i * 60 * 10))):
#                 count = count+1
#         plt_array.append((i * 10, count))
#         print(f"{(i * 10)} {count}")
#     plotData(plt, plt_array, fc)
# plt.title('djpeg')
# plt.ylabel('path')
# plt.xlabel('time(ms)')
# plt.legend(loc='best')
# plt.show()

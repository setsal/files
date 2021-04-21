import os
import sys
import time
import matplotlib.pyplot as plt
import glob
import subprocess
from collections import Counter
import numpy as np
import click


def plotData(plt, data, t):
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    if(t == 0):
        plt.plot(x, y, '-', label='AFLNET')
    elif(t == 1):
        plt.plot(x, y, '-', label='AFLDEV')
    elif(t == 2):
        plt.plot(x, y, '-', label='AFLNWE')


def calData(fuzzerDir, file_num, time):
    dirpath = fuzzerDir
    file_list = [os.path.basename(x)
                 for x in glob.glob(dirpath+"/trace_data/id*")]
    file_list.sort()

    time_array = []

    if 'aflnwe' in dirpath:
        testDir = '/queue/'
    else:
        testDir = '/replayable-queue/'

    for f in file_list:
        mofidy_time = int(os.path.getmtime(dirpath + testDir + f))
        time_array.append(mofidy_time)

    basetime = time_array[0]
    raw_bitmap = {}
    tmp_cnt = []

    trace_data_raw = ''
    for i in range(len(file_list)):
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
    plotData(plt, plt_array, file_num)


@click.command()
@click.option('-n', '--num', 'fuzzer_num', help='Number of fuzzer', type=int, default=3, show_default=True)
@click.option('-s', '--second', 'second', help='time(second)', type=int, default=3600, show_default=True)
@click.option('-d', '--des', 'des', help='target', type=str, required=True)
@click.option('-p', '--protocol', 'protocol', help='protocol', required=True)
def main(fuzzer_num, second, des, protocol):

    fuzzer1 = "out-" + des + "-aflnet"
    fuzzer2 = "out-" + des + "-afldev"
    fuzzer3 = "out-" + des + "-aflnwe"

    time = int(second/600)

    # Calculate
    calData(fuzzer1, 0, time)
    calData(fuzzer2, 1, time)
    # calData(fuzzer3, 2, time)

    # Draw
    plt.title(des + '(' + protocol + ')' + ' - ' + str(second))
    plt.ylabel('Edge Coverage')
    plt.xlabel('Time (minute)')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    main()

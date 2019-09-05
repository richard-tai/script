#!/usr/bin/env python

import sys
import datetime
import time
import os

def get_n_float(f_str, n=1):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return ".".join([a, c])

def get_timestamp(time_str, time_format="%Y-%m-%d %H:%M:%S"):
    timeArray = time.strptime(time_str, time_format)
    return time.mktime(timeArray)

def get_work_duration(duration):
    duration /= 3600
    if duration > 5:
        duration -= 1
    #if duration > 10:
        #duration -= 1
    return duration

def record(start_time, refresh=False):
    today=datetime.date.today()

    start_time_full = "{0} {1}".format(today, start_time)
    start_timestamp = get_timestamp(start_time_full, "%Y-%m-%d %H:%M")
    #print("start timestamp: {0}".format(start_timestamp))

    end_timestamp = time.time()
    work_duration = get_work_duration(end_timestamp - start_timestamp)

    start_time_str = time.strftime("%H:%M:%S", time.localtime(start_timestamp))
    end_time_str = time.strftime("%H:%M:%S", time.localtime(end_timestamp))

    header_str = "{0:10}  {1:8}  {2:8}  {3}\n".format("Date", "Come", "Leave", "Hour")
    output_str = "{0}  {1}  {2}  {3}\n".format(today, start_time_str, end_time_str, get_n_float(work_duration, 1))
    #print("{0}".format(output_str))

    log_path = "log.text"
    
        all_lines = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            all_lines = f.readlines()
            if len(all_lines) > 0 and all_lines[-1].startswith(str(today)):
                all_lines[-1] = output_str
            else:
                all_lines.append(output_str)

    num_limit = 32
    if len(all_lines) > num_limit:
        all_lines = all_lines[-num_limit:]
    with open(log_path, "w") as f:
        f.write(header_str)
        print("{0}".format(header_str.strip()))
        is_first_line = True
        for one in all_lines:
            if is_first_line:
                is_first_line = False
                continue
            one_str = one
            if refresh:
                one_list = one.split('  ')
                #print("{0} {1} {2}".format(one_list[0], one_list[1], one_list[2]))
                one_start = get_timestamp("{0} {1}".format(one_list[0], one_list[1]))
                one_end = get_timestamp("{0} {1}".format(one_list[0], one_list[2]))
                one_work_duration = get_work_duration(one_end - one_start)
                one_list[3] = get_n_float(one_work_duration, 1)
                one_str = '  '.join(one_list)
                one_str += '\n'
            f.write(one_str)
            print("{0}".format(one_str.strip()))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {0} {1}".format(sys.argv[0], "9:30:00"))
        exit(0)
    refresh = False
    if len(sys.argv) >=3:
        refresh = bool(sys.argv[2])
    record(sys.argv[1], refresh)

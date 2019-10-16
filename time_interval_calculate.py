import os
import json
import datetime

filename_in_list = ["logs_out/session_143/session_143_alarm.log",
                    "logs_out/session_144/session_144_alarm.log",
                    "logs_out/session_145/session_145_alarm.log",
                    "logs_out/session_146/session_146_alarm.log",
                    "logs_out/session_147/session_147_alarm.log",
                    "logs_out/session_148/session_148_alarm.log",
                    "logs_out/session_149/session_149_alarm.log",
                    "logs_out/session_150/session_150_alarm.log",
                    "logs_out/session_151/session_151_alarm.log",
                    "logs_out/session_362/session_362_alarm.log"]

for filename_in in filename_in_list:
    print("Calculate", filename_in)

    filename_out = "{0:s}/{1:s}_time_interval.log".format(os.path.split(filename_in)[0], filename_in.split('/')[-1][:-10])

    with open(filename_in, 'r') as file_in:
        line_list = json.load(file_in)
        time_list = (line[:-1] for line in line_list)

        interval_list = []
        time_prev = None
        for time in time_list:
            if time_prev is not None:
                interval = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f') - time_prev
                interval_list.append(f"{interval.seconds + interval.microseconds / 1000000}\n")
            time_prev = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f')

    with open(filename_out, 'w') as file_out:
        file_out.writelines(interval_list)

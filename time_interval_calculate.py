import os
import json
import datetime

start_time_list = ["26.09.2019 05:36:16.0",
                   "26.09.2019 07:03:54.0",
                   "26.09.2019 07:27:52.0",
                   "28.09.2019 23:01:16.0",
                   "28.09.2019 23:42:05.0",
                   "29.09.2019 00:21:23.0",
                   "14.10.2019 21:07:23.0",
                   "14.10.2019 21:25:24.0",
                   "14.10.2019 21:44:48.0",
                   "14.10.2019 21:59:00.0",
                   "14.10.2019 22:14:09.0",
                   "14.10.2019 22:30:01.0",
                   "14.10.2019 22:39:51.0",
                   "14.10.2019 23:07:56.0",
                   "14.10.2019 23:27:27.0"]

filename_alarm_list = ["logs_out/session_360/session_360_alarm.log",
                       "logs_out/session_361/session_361_alarm.log",
                       "logs_out/session_362/session_362_alarm.log",
                       "logs_out/session_409/session_409_alarm.log",
                       "logs_out/session_410/session_410_alarm.log",
                       "logs_out/session_411/session_411_alarm.log",
                       "logs_out/session_143/session_143_alarm.log",
                       "logs_out/session_144/session_144_alarm.log",
                       "logs_out/session_145/session_145_alarm.log",
                       "logs_out/session_146/session_146_alarm.log",
                       "logs_out/session_147/session_147_alarm.log",
                       "logs_out/session_148/session_148_alarm.log",
                       "logs_out/session_149/session_149_alarm.log",
                       "logs_out/session_150/session_150_alarm.log",
                       "logs_out/session_151/session_151_alarm.log"]
filename_unreset_list = ["logs_out/session_360/session_360_unreset.log",
                         "logs_out/session_361/session_361_unreset.log",
                         "logs_out/session_362/session_362_unreset.log",
                         "logs_out/session_409/session_409_unreset.log",
                         "logs_out/session_410/session_410_unreset.log",
                         "logs_out/session_411/session_411_unreset.log",
                         "logs_out/session_143/session_143_unreset.log",
                         "logs_out/session_144/session_144_unreset.log",
                         "logs_out/session_145/session_145_unreset.log",
                         "logs_out/session_146/session_146_unreset.log",
                         "logs_out/session_147/session_147_unreset.log",
                         "logs_out/session_148/session_148_unreset.log",
                         "logs_out/session_149/session_149_unreset.log",
                         "logs_out/session_150/session_150_unreset.log",
                         "logs_out/session_151/session_151_unreset.log"]
filename_irq_mem_list = ["logs_out/session_360/session_360_irq_mem.log",
                         "logs_out/session_361/session_361_irq_mem.log",
                         "logs_out/session_362/session_362_irq_mem.log",
                         "logs_out/session_409/session_409_irq_mem.log",
                         "logs_out/session_410/session_410_irq_mem.log",
                         "logs_out/session_411/session_411_irq_mem.log",
                         "logs_out/session_143/session_143_irq_mem.log",
                         "logs_out/session_144/session_144_irq_mem.log",
                         "logs_out/session_145/session_145_irq_mem.log",
                         "logs_out/session_146/session_146_irq_mem.log",
                         "logs_out/session_147/session_147_irq_mem.log",
                         "logs_out/session_148/session_148_irq_mem.log",
                         "logs_out/session_149/session_149_irq_mem.log",
                         "logs_out/session_150/session_150_irq_mem.log",
                         "logs_out/session_151/session_151_irq_mem.log"]
filename_err2_mem_list = ["logs_out/session_360/session_360_err2_mem.log",
                          "logs_out/session_361/session_361_err2_mem.log",
                          "logs_out/session_362/session_362_err2_mem.log",
                          "logs_out/session_409/session_409_err2_mem.log",
                          "logs_out/session_410/session_410_err2_mem.log",
                          "logs_out/session_411/session_411_err2_mem.log",
                          "logs_out/session_143/session_143_err2_mem.log",
                          "logs_out/session_144/session_144_err2_mem.log",
                          "logs_out/session_145/session_145_err2_mem.log",
                          "logs_out/session_146/session_146_err2_mem.log",
                          "logs_out/session_147/session_147_err2_mem.log",
                          "logs_out/session_148/session_148_err2_mem.log",
                          "logs_out/session_149/session_149_err2_mem.log",
                          "logs_out/session_150/session_150_err2_mem.log",
                          "logs_out/session_151/session_151_err2_mem.log"]


def create_list_times(filename_in_list, filename_out_list, start_list):
    for filename_in, filename_out, start in zip(filename_in_list, filename_out_list, start_list):
        print("Calculate", filename_in)

        with open(filename_in, 'r') as file_in:
            line_list = json.load(file_in)
            time_list = (line[0] if type(line_list[0]) is list else line for line in line_list)

            interval_list = []
            time_prev = datetime.datetime.strptime(start, '%d.%m.%Y %H:%M:%S.%f')
            for time in time_list:
                # if time_prev is not None:
                interval = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f') - time_prev
                interval_list.append(f"{interval.seconds + interval.microseconds / 1000000}\n")
                time_prev = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f')

        average = sum([float(time[:-1]) for time in interval_list]) / len(interval_list) if len(
            interval_list) != 0 else 0

        with open(filename_out, 'w') as file_out:
            file_out.writelines(interval_list)
            file_out.write("average = {0:f}\n".format(average))


create_list_times(filename_alarm_list,
                  ["{0:s}/{1:s}_time_interval_alarm.log".format(os.path.split(name)[0], name.split('/')[-1][:-10]) for
                   name in filename_alarm_list], start_time_list)
create_list_times(filename_unreset_list,
                  ["{0:s}/{1:s}_time_interval_reset.log".format(os.path.split(name)[0], name.split('/')[-1][:-12]) for
                   name in filename_unreset_list], start_time_list)
create_list_times(filename_irq_mem_list,
                  ["{0:s}/{1:s}_time_interval_irq_mem.log".format(os.path.split(name)[0], name.split('/')[-1][:-12])
                   for name in filename_irq_mem_list], start_time_list)
create_list_times(filename_err2_mem_list,
                  ["{0:s}/{1:s}_time_interval_err2_mem.log".format(os.path.split(name)[0], name.split('/')[-1][:-13])
                   for name in filename_err2_mem_list], start_time_list)

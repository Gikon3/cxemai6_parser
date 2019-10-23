import os
import json
import datetime

filename_alarm_list = ["logs_out/session_143/session_143_alarm.log",
                       "logs_out/session_144/session_144_alarm.log",
                       "logs_out/session_145/session_145_alarm.log",
                       "logs_out/session_146/session_146_alarm.log",
                       "logs_out/session_147/session_147_alarm.log",
                       "logs_out/session_148/session_148_alarm.log",
                       "logs_out/session_149/session_149_alarm.log",
                       "logs_out/session_150/session_150_alarm.log",
                       "logs_out/session_151/session_151_alarm.log",
                       "logs_out/session_362/session_362_alarm.log"]
filename_unreset_list = ["logs_out/session_143/session_143_unreset.log",
                         "logs_out/session_144/session_144_unreset.log",
                         "logs_out/session_145/session_145_unreset.log",
                         "logs_out/session_146/session_146_unreset.log",
                         "logs_out/session_147/session_147_unreset.log",
                         "logs_out/session_148/session_148_unreset.log",
                         "logs_out/session_149/session_149_unreset.log",
                         "logs_out/session_150/session_150_unreset.log",
                         "logs_out/session_151/session_151_unreset.log"]
filename_irq_mem_list = ["logs_out/session_143/session_143_irq_mem.log",
                         "logs_out/session_144/session_144_irq_mem.log",
                         "logs_out/session_145/session_145_irq_mem.log",
                         "logs_out/session_146/session_146_irq_mem.log",
                         "logs_out/session_147/session_147_irq_mem.log",
                         "logs_out/session_148/session_148_irq_mem.log",
                         "logs_out/session_149/session_149_irq_mem.log",
                         "logs_out/session_150/session_150_irq_mem.log",
                         "logs_out/session_151/session_151_irq_mem.log"]


def create_list_times(filename_in_list, filename_out_list):
    for filename_in, filename_out in zip(filename_in_list, filename_out_list):
        print("Calculate", filename_in)

        with open(filename_in, 'r') as file_in:
            time_list = (line for line in json.load(file_in))

            interval_list = []
            time_prev = None
            for time in time_list:
                if time_prev is not None:
                    interval = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f') - time_prev
                    interval_list.append(f"{interval.seconds + interval.microseconds / 1000000}\n")
                time_prev = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f')

        average = sum([float(time[:-1]) for time in interval_list]) / len(interval_list)

        with open(filename_out, 'w') as file_out:
            file_out.writelines(interval_list)
            file_out.write("average = {0:f}\n".format(average))


def create_list_times2(filename_in_list, filename_out_list):
    for filename_in in filename_irq_mem_list:
        print("Calculate", filename_in)

        filename_out = "{0:s}/{1:s}_time_interval_irq_mem.log".format(os.path.split(filename_in)[0],
                                                                      filename_in.split('/')[-1][:-12])

        with open(filename_in, 'r') as file_in:
            line_list = json.load(file_in)
            time_list = (line[0] for line in line_list)

            interval_list = []
            time_prev = None
            for time in time_list:
                if time_prev is not None:
                    interval = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f') - time_prev
                    interval_list.append(f"{interval.seconds + interval.microseconds / 1000000}\n")
                time_prev = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M:%S.%f')

        average = sum([float(time[:-1]) for time in interval_list]) / len(interval_list)

        with open(filename_out, 'w') as file_out:
            file_out.writelines(interval_list)
            file_out.write("average = {0:f}\n".format(average))


create_list_times(filename_alarm_list,
                  ["{0:s}/{1:s}_time_interval_alarm.log".format(os.path.split(name)[0], name.split('/')[-1][:-10]) for
                   name in filename_alarm_list])
create_list_times(filename_unreset_list,
                  ["{0:s}/{1:s}_time_interval_reset.log".format(os.path.split(name)[0], name.split('/')[-1][:-12]) for
                   name in filename_unreset_list])

create_list_times2(filename_irq_mem_list,
                   ["{0:s}/{1:s}_time_interval_irq_mem.log".format(os.path.split(name)[0], name.split('/')[-1][:-12])
                    for name in filename_irq_mem_list])

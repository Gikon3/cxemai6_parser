import datetime
import json

from defines import *

filename_in_list = ["unnecessary/sum_184_unnecessary.log",
                    # "unnecessary/U_18.09.2019_23-39-09_parse_unnecessary.log"]
                    "logs_in/session_184/sum_184.log"]
filename_out_list = ["unnecessary/session_184/temp/sum_184_unnecessary_processed.log",
                     "unnecessary/session_186/temp/U_18.09.2019_23-39-09_parse_unnecessary_processed.log"]
filename_addresses = "technical_info/addresses.txt"

with open(filename_addresses, 'r') as file_addr:
    blocks_addresses = json.load(file_addr)

for filename_in, filename_out in zip(filename_in_list, filename_out_list):
    with open(filename_in, 'r') as file_in:
        lines = json.load(file_in)

    data = [["{0:26s} F0DAE000".format("_" * 26),
             "{0:26s} aaaaaaaa".format("_" * 26),
             "{0:26s} {1:8s}".format("_" * 26, COM_MEM0_READ_start),
             ""]]
    count = 0
    count_packages = 0
    count_errors = 0
    last_time = None
    while True:
        try:
            if lines[count][-8:] in blocks_addresses and blocks_addresses[lines[count][-8:]] == "memory":
                time_now = datetime.datetime.strptime(lines[count][:26], '%d.%m.%Y %H:%M:%S.%f')
                if last_time is None or (time_now - last_time).microseconds + (time_now - last_time).seconds * 1000000 < 1000000:
                    last_time = datetime.datetime.strptime(lines[count][:26], '%d.%m.%Y %H:%M:%S.%f')
                    data[count_packages].append(lines[count])
                    data[count_packages].append(lines[count + 1])
                    count_errors += 1
                    count += 2
                else:
                    last_time = datetime.datetime.strptime(lines[count][:26], '%d.%m.%Y %H:%M:%S.%f')
                    data[count_packages][3] = "{0:26s} {1:08X}".format("_" * 26, count_errors)
                    count_errors = 1
                    count_packages += 1
                    data.append(["{0:26s} F0DAE000".format("_" * 26),
                                 "{0:26s} aaaaaaaa".format("_" * 26),
                                 "{0:26s} {1:8s}".format("_" * 26, COM_MEM0_READ_start),
                                 ""])
                    data[count_packages].append(lines[count])
                    data[count_packages].append(lines[count + 1])
                    count += 1

            else:
                count += 1

        except IndexError:
            break

    with open(filename_out, 'w') as file_out:
        for frame in data:
            for line in frame:
                file_out.write(line + "\n")
            # json.dump(data, file_out, indent=2)

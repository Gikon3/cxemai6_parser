import os
import json

from defines import *

# filename_in_list = ["logs_in/session_184/sum_184.log",
#                     "logs_in/session_186/U_18.09.2019_23-39-09_parse.log"]
# filename_in_list = ["logs_in/session_360/U_26.09.2019_05-11-54.log",
#                     "logs_in/session_361/U_26.09.2019_06-56-58.log",
#                     "logs_in/session_362/U_26.09.2019_07-18-06.log",
#                     "logs_in/session_409/summary_409_death.log",
#                     "logs_in/session_410/U_28.09.2019_23-41-46.log",
#                     "logs_in/session_411/U_29.09.2019_00-21-12.log"]
filename_in_list = ["logs_in/session_143/U_14.10.2019_21-03-38.log",
                    "logs_in/session_144/U_14.10.2019_21-23-18.log",
                    "logs_in/session_145/U_14.10.2019_21-44-54.log",
                    "logs_in/session_146/U_14.10.2019_21-59-01.log",
                    "logs_in/session_147/U_14.10.2019_22-14-16.log",
                    "logs_in/session_148/U_14.10.2019_22-30-06.log",
                    "logs_in/session_149/U_14.10.2019_22-39-54.log",
                    "logs_in/session_150/U_14.10.2019_23-01-49.log",
                    "logs_in/session_151/U_14.10.2019_23-22-24.log"]
filename_addresses = "technical_info/addresses.txt"

# alignment packages
print("Alignment:")
filename_alignment = []
for filename_in in filename_in_list:
    print("  Calculate", filename_in)
    filename_out = "{0:s}/temp/{1:s}_alignment.log".format(os.path.split(filename_in)[0],
                                                           os.path.splitext(filename_in)[0].split('/')[-1])
    filename_alignment.append(filename_out)

    with open(filename_in, 'r') as file_in:
        lines_in = file_in.readlines()

    long_lines = []
    for i, line in enumerate(lines_in):
        if len(line) != 36:
            long_lines.append(i)

    for i in long_lines:
        if len(lines_in[i]) > 36:
            lines_in[i] = "{0:s}\n{1:8s} {2:8s}\n".format(lines_in[i][:35], lines_in[i + 1][:26], lines_in[i][35:-1])
        else:
            lines_in[i] = "{0:s} {1:<8s}\n".format(lines_in[i][:26], lines_in[i][27:-1])

    with open(filename_out, 'w') as file_out:
        file_out.writelines(lines_in)

    with open(filename_out, 'r') as file_out:
        for i, line in enumerate(file_out.readlines()):
            if len(line) != 36:
                print(i + 1)

print("")

# delete bad packages
with open(filename_addresses, 'r') as file_addr:
    blocks_addresses = json.load(file_addr)

addresses = [addr for addr in blocks_addresses]

print("Delete bad packages:")
filename_correct = []
for filename_in in filename_alignment:
    print("  Calculate", filename_in)

    filename_out = "{0:s}_correct.log".format(os.path.splitext(filename_in)[0][:-10])
    filename_correct.append(filename_out)

    with open(filename_in, 'r') as file_in:
        lines_in = file_in.readlines()

    print("   ", len(lines_in), end=" -> ")

    rave = []
    del_time = []
    count = 0
    number_errors = None
    while True:
        try:
            if lines_in[count][27:35] == COM_FLAG_ERROR:
                time_last = lines_in[count][:26] if lines_in[count][:26] != "_" * 26 else lines_in[count + 1][:26]
                count_last = count
                count += 1

                # number epoch
                count += 1

                # module
                count += 1

                number_errors = int(lines_in[count][27:35], 16)
                number_errors = number_errors if (number_errors * 2) < (THRESHOLD_ERRORS * 2) else THRESHOLD_ERRORS
                count += 1

                flag_delete = False
                for errors_count in range(number_errors):
                    if lines_in[count][27:35] not in addresses:
                        flag_delete = True

                    if lines_in[count][27:35] == COM_ALRM_TMR \
                            or lines_in[count][27:35] == COM_UNRESET_DEVICE:
                        count += 1
                        break

                    elif lines_in[count + 1][27:35] == COM_ALRM_TMR \
                            or lines_in[count + 1][27:35] == COM_UNRESET_DEVICE:
                        count += 2
                        break

                    elif lines_in[count][27:35] == COM_FLAG_ERROR:
                        del_time.append([time_last, lines_in[count][:26] if lines_in[count][:26] != "_" * 26 \
                            else lines_in[count - 1][:26]])
                        del lines_in[count_last:count]
                        count = count_last - 1
                        break

                    elif lines_in[count + 1][27:35] == COM_FLAG_ERROR:
                        del_time.append([time_last, lines_in[count + 1][:26] if lines_in[count + 1][:26] != "_" * 26 \
                            else lines_in[count][:26]])
                        del lines_in[count_last:count + 1]
                        count = count_last - 1
                        break

                    count += 2

                if flag_delete is True:
                    del_time.append([time_last, lines_in[count + 1][:26] if lines_in[count + 1][:26] != "_" * 26 \
                        else lines_in[count][:26]])
                    del lines_in[count_last:count - 1]
                    count = count_last - 1

                # count += 1
            elif lines_in[count][27:35] == COM_OK:
                count += 2

            elif lines_in[count][27:35] == COM_UNRESET_DEVICE \
                    or lines_in[count][27:35] == COM_ALRM_TMR \
                    or lines_in[count][27:35] == COM_err_CORR_IRQ \
                    or lines_in[count][27:35] == COM_TIMEOUT_SPI \
                    or lines_in[count][27:35] == COM_STM_START:
                count += 1

            elif lines_in[count][27:35] == COM_MEM_IRQ_start:
                count += 3

            else:
                rave.append(lines_in[count][:-1])
                count += 1

        except IndexError:
            break

    print("{0:d}, deleted {1:d} packets".format(len(lines_in), len(del_time)))

    with open(filename_out, 'w') as file_out:
        file_out.writelines(lines_in)

    with open("{0:s}_remove_packages.log".format(os.path.splitext(filename_out)[0][:-10]), 'w') as file_del_pack:
        json.dump(del_time, file_del_pack, indent=2)

    with open("unnecessary/{0:s}_unnecessary.log".format(os.path.split(os.path.splitext(filename_out)[0][:-8])[-1]),
              'w') as file_rave:
        json.dump(rave, file_rave, indent=2)

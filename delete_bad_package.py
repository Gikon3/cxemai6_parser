import os
import json

from defines import *

filename_in_list = ["logs_in/session_409/temp/summary_409_alignment.log",
                    "logs_in/session_410/temp/U_28.09.2019_23-41-46_alignment.log",
                    "logs_in/session_411/temp/U_29.09.2019_00-21-12_alignment.log"]
filename_addresses = "addresses.txt"

with open(filename_addresses, 'r') as file_addr:
    blocks_addresses = json.load(file_addr)

addresses = [addr for addr in blocks_addresses]

for filename_in in filename_in_list:
    print("Calculate", filename_in)

    filename_delete_pack = "{0:s}/time_deleted_packages.log".format(os.path.split(filename_in)[0])

    with open(filename_in, 'r') as file_in:
        lines_in = file_in.readlines()

    print(len(lines_in), end=" -> ")

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

                # if lines_in[count + 1][27:35] != COM_FLAG_ERROR\
                #         and lines_in[count + 1][27:35] != COM_UNRESET_DEVICE\
                #         and lines_in[count + 1][27:35] != COM_OK \
                #         and lines_in[count + 1][27:35] != COM_ALRM_TMR \
                #         and lines_in[count + 1][27:35] != COM_ERR2_MEM \
                #         and lines_in[count + 1][27:35] != COM_err_CORR_IRQ \
                #         and lines_in[count + 1][27:35] != COM_TIMEOUT_SPI:
                #     count += 1
                #     while lines_in[count][27:35] != COM_FLAG_ERROR:
                #         count += 1
                #
                #     del_time.append([time_last, lines_in[count - 1][:26] if lines_in[count - 1][:26] != "_" * 26 \
                #         else lines_in[count][:26]])
                #     del lines_in[count_last:count - 1]

            # elif lines_in[count][27:35] == COM_OK:
            #     count += 2
            #
            # elif lines_in[count][27:35] == COM_MEM_IRQ_start:
            #     count += 3
            #
            # elif lines_in[count][27:35] == COM_ALRM_TMR \
            #         or lines_in[count][27:35] == COM_UNRESET_DEVICE\ 28.09.2019 23:14:29.488372 F0DAE000
            #         or lines_in[count][27:35] == COM_ERR2_MEM\ 28.09.2019 23:14:29.511311 F0DAE000
            #         or lines_in[count][27:35] == COM_err_CORR_IRQ\
            #         or lines_in[count][27:35] == COM_TIMEOUT_SPI:
            #     count += 1
            #
            # elif lines_in[count][27:35] == COM_RAVE:
            #     count += 3

        except IndexError:
            break

    print("{0:d}, deleted {1:d} packets".format(len(lines_in), len(del_time)))

    with open(filename_in, 'w') as file_out:
        file_out.writelines(lines_in)

    with open(filename_delete_pack, 'w') as file_del_pack:
        json.dump(del_time, file_del_pack, indent=2)

    with open("rave/rave_{0:s}".format(os.path.split(filename_in)[1]), 'w') as file_rave:
        json.dump(rave, file_rave, indent=2)

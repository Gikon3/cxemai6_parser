import os
import json
import operator

from defines import *

filename_in_list = ["logs_in/session_360/temp/U_26.09.2019_05-11-54_correct.log",
                    "logs_in/session_361/temp/U_26.09.2019_06-56-58_correct.log",
                    "logs_in/session_362/temp/U_26.09.2019_07-18-06_correct.log",
                    "logs_in/session_409/temp/summary_409_correct.log",
                    "logs_in/session_410/temp/U_28.09.2019_23-41-46_correct.log",
                    "logs_in/session_411/temp/U_29.09.2019_00-21-12_correct.log"]

filename_reference = "technical_info/reference.txt"
filename_addresses = "technical_info/addresses.txt"


def mem_reference(word, word_ref):
    return word_ref if word_ref.upper() != "XXXXXXXX" else "55555555" if word.count("5") > word.upper().count("A") \
        else "AAAAAAAA"


with open(filename_addresses, 'r') as file_addr:
    blocks_addresses = json.load(file_addr)

with open(filename_reference, 'r') as file_ref:
    reference = json.load(file_ref)

for filename_in in filename_in_list:
    print("Calculate", filename_in)

    filename_parse = "logs_out/{0:s}/{1:s}_config.log".format(filename_in.split('/')[-3], filename_in.split('/')[-3])

    with open(filename_in, 'r') as file_in:
        lines_in = file_in.readlines()

    # Remove COM_OK
    count = 0
    while True:
        try:
            if lines_in[count][27:35] == COM_OK:
                lines_in.pop(count)  # COM_OK
                lines_in.pop(count)  # Epoch

            else:
                count += 1

        except IndexError:
            break

    # IRQ memory
    count = 0
    irq_mem = []
    while True:
        try:
            if lines_in[count][27:35] == COM_MEM_IRQ_start:
                lines_in.pop(count)
                irq_mem.append([lines_in[count][:26], lines_in.pop(count)[27:35], lines_in.pop(count)[27:35]])

            else:
                count += 1

        except IndexError:
            break

    filename_irq_mem = "{0:s}/{1:s}_irq_mem.log".format(os.path.split(filename_parse)[0], filename_in.split('/')[-3])
    with open(filename_irq_mem, 'w') as file_irq_mem:
        json.dump(irq_mem, file_irq_mem, indent=2)

    del irq_mem
    del filename_irq_mem
    del file_irq_mem

    # ALARM TIMER worked
    count = 0
    alarm = []
    while True:
        try:
            if lines_in[count][27:35] == COM_ALRM_TMR:
                alarm.append(lines_in[count][:26])
                # lines_in.pop(count)
                count += 1

            else:
                count += 1

        except IndexError:
            break

    filename_alarm = "{0:s}/{1:s}_alarm.log".format(os.path.split(filename_parse)[0], filename_in.split('/')[-3])
    with open(filename_alarm, 'w') as file_alarm:
        json.dump(alarm, file_alarm, indent=2)

    del alarm
    del filename_alarm
    del file_alarm

    # Unreset
    count = 0
    unreset = []
    while True:
        try:
            if lines_in[count][27:35] == COM_UNRESET_DEVICE:
                unreset.append(lines_in[count][:26])
                # lines_in.pop(count)
                count += 1

            else:
                count += 1

        except IndexError:
            break

    filename_unreset = "{0:s}/{1:s}_unreset.log".format(os.path.split(filename_parse)[0], filename_in.split('/')[-3])
    with open(filename_unreset, 'w') as file_unreset:
        json.dump(unreset, file_unreset, indent=2)

    del unreset
    del filename_unreset
    del file_unreset

    # err_CORR_IRQ
    count = 0
    err_corr_irq = []
    while True:
        try:
            if lines_in[count][27:35] == COM_err_CORR_IRQ:
                err_corr_irq.append(lines_in.pop(count)[:26])
                count += 1

            else:
                count += 1

        except IndexError:
            break

    filename_err_corr_irq = "{0:s}/{1:s}_err_corr.log".format(os.path.split(filename_parse)[0],
                                                              filename_in.split('/')[-3])
    with open(filename_err_corr_irq, 'w') as file_err_corr_irq:
        json.dump(err_corr_irq, file_err_corr_irq, indent=2)

    del err_corr_irq
    del filename_err_corr_irq
    del file_err_corr_irq

    # main parse
    count = 0
    errors = {}
    repeat_packages = []
    memory_failure_coord_package = []
    memory_failure_coord_package_list = []
    while True:
        try:
            if lines_in[count][27:35] == COM_FLAG_ERROR:
                count += 1

                # number epoch
                count += 1

                # module
                count += 1

                number_errors = int(lines_in[count][27:35], 16)
                number_errors = number_errors if (number_errors * 2) < (THRESHOLD_ERRORS * 2) else THRESHOLD_ERRORS
                count += 1

                memory_failure_coord_package = []
                for errors_count in range(number_errors):
                    if lines_in[count][27:35] == COM_ALRM_TMR \
                            or lines_in[count][27:35] == COM_UNRESET_DEVICE:
                        count += 1
                        repeat_packages = []
                        break

                    elif lines_in[count + 1][27:35] == COM_ALRM_TMR \
                            or lines_in[count + 1][27:35] == COM_UNRESET_DEVICE:
                        count += 2
                        repeat_packages = []
                        break

                    if lines_in[count][27:35] not in errors.keys():
                        errors[lines_in[count][27:35]] = []
                    if errors_count < number_errors:
                        try:
                            reference_xor_word = "{0:032b}".format(operator.xor(
                                int(lines_in[count + 1][27:35], 16),
                                int(mem_reference(lines_in[count + 1][27:35],
                                                  reference[lines_in[count][27:35]]), 16)))
                            if [lines_in[count][27:35], lines_in[count + 1][27:35]] not in repeat_packages:
                                errors[lines_in[count][27:35]].append([lines_in[count][:26],
                                                                       lines_in[count + 1][27:35],
                                                                       reference[lines_in[count][27:35]],
                                                                       reference_xor_word])

                                if blocks_addresses[lines_in[count][27:35]] == "memory":
                                    for i, symbol in enumerate(reference_xor_word[::-1]):
                                        if symbol == "1":
                                            address_bin = "{0:032b}".format(int(lines_in[count][27:35], 16))
                                            memory_failure_coord_package.append(
                                                [int(address_bin[-5:-2], 2) * (i + 1),
                                                 int(address_bin[-21:-6], 2)])
                                    # if reference_xor_word.count("1") > 1:
                                    #     print(lines_in[count][:35])
                                    #     print(lines_in[count + 1][:35])

                                if blocks_addresses[lines_in[count][27:35]] == "channels_accumulate" \
                                        or blocks_addresses[lines_in[count][27:35]] == "tlm":
                                    repeat_packages.append([lines_in[count][27:35], lines_in[count + 1][27:35]])

                        except KeyError:
                            print(number_errors, errors_count)
                            print(lines_in[count - 1][:-1])
                            print(lines_in[count][:-1])
                            exit("KeyError")

                        count += 2

            elif lines_in[count][27:35] == COM_UNRESET_DEVICE:
                count += 1
                repeat_packages = []

            else:
                count += 1

            if len(memory_failure_coord_package) > 0:
                memory_failure_coord_package_list.append(memory_failure_coord_package)
                memory_failure_coord_package = []

        except IndexError:
            break

    lines_parse = {'alrm_tmr': {}, 'channels_config': {}, 'channels_accumulate': {}, 'fts': {}, 'gpio': {}, 'inmux': {},
                   'pll': {}, 'spim4': {}, 'tlm': {}, 'tmr1': {}, 'tsm': {}, 'uart1': {}, 'uart2': {}, 'memory': {}}
    for address in errors.keys():
        lines_parse[blocks_addresses[address]][address] = errors[address]

    for block in lines_parse.keys():
        for address in lines_parse[block].keys():
            for error_frame in lines_parse[block][address]:
                if error_frame[1][:4] == "F0DA":
                    print(address)
                    exit()

    with open(filename_parse, 'w') as file_parse:
        json.dump(lines_parse, file_parse, indent=2)

    filename_memory_failure_coord = "{0:s}/{1:s}_memory_failure_coord.log".format(os.path.split(filename_parse)[0],
                                                                                  filename_in.split('/')[-3])
    with open(filename_memory_failure_coord, 'w') as file_memory_failure_coord:
        # json.dump(memory_failure_coord_package_list, file_memory_failure_coord, indent=2)
        for line in memory_failure_coord_package_list:
            file_memory_failure_coord.write(str(line) + "\n")

    # calculate number errors
    filename_number_errors = "{0:s}_number_errors.log".format(os.path.splitext(filename_parse)[0][:-7])

    errors_dict = lines_parse.copy()
    lines_out = {'alrm_tmr': {}, 'channels_config': {}, 'channels_accumulate': {}, 'fts': {}, 'gpio': {}, 'inmux': {},
                 'pll': {}, 'spim4': {}, 'tlm': {}, 'tmr1': {}, 'tsm': {}, 'uart1': {}, 'uart2': {}, 'memory': {}}
    for module in errors_dict:
        for address in errors_dict[module]:
            lines_out[module][address] = sum([int(xor[3].count("1")) for xor in errors_dict[module][address]])

    errors_all = {}
    for module in lines_out:
        errors_all[module] = sum([lines_out[module][address] for address in lines_out[module]])

    with open(filename_number_errors, 'w') as file_number_errors:
        file_number_errors.write(filename_parse + "\n")
        json.dump(lines_out, file_number_errors, indent=2)
        file_number_errors.write("\n")
        json.dump(errors_all, file_number_errors, indent=2)

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

filename_reference = "reference.txt"
filename_addresses = "addresses.txt"


def mem_reference(word, word_ref):
    return word_ref if word_ref.upper() != "XXXXXXXX" else "55555555" if word.count("5") > word.upper().count("A") \
        else "AAAAAAAA"


with open(filename_addresses, 'r') as file_addr:
    blocks_addresses = json.load(file_addr)

with open(filename_reference, 'r') as file_ref:
    reference = json.load(file_ref)

for filename_in in filename_in_list:
    print("Calculate", filename_in)

    filename_out = "logs_out/{0:s}/{1:s}_config.log".format(filename_in.split('/')[-3], filename_in.split('/')[-3])

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

    filename_irq_mem = "{0:s}/{1:s}_irq_mem.log".format(os.path.split(filename_out)[0], filename_in.split('/')[-3])
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

    filename_alarm = "{0:s}/{1:s}_alarm.log".format(os.path.split(filename_out)[0], filename_in.split('/')[-3])
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

    filename_unreset = "{0:s}/{1:s}_unreset.log".format(os.path.split(filename_out)[0], filename_in.split('/')[-3])
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

    filename_err_corr_irq = "{0:s}/{1:s}_err_corr.log".format(os.path.split(filename_out)[0],
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
                                # if 0x40001000 <= int(lines_in[count][27:35], 16) < 0x40009000:
                                #     if 0x00 <= int(lines_in[count][33:35], 16) < 0x48:
                                #         if lines_in[count][27:35] not in errors.keys():
                                #             errors[lines_in[count][27:35]] = []
                                errors[lines_in[count][27:35]].append([lines_in[count][:26],
                                                                       lines_in[count + 1][27:35],
                                                                       reference[lines_in[count][27:35]],
                                                                       reference_xor_word])
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

        except IndexError:
            break

    # lines_out = {'alrm_tmr': {}, 'channels_config': {}, 'channels_accumulate': {}, 'fts': {}, 'gpio': {}, 'inmux': {},
    #              'pll': {}, 'spim4': {}, 'tlm': {}, 'tmr1': {}, 'tsm': {}, 'uart1': {}, 'uart2': {}, 'memory': {}}
    lines_out = {'alrm_tmr': {}, 'channels': {}, 'fts': {}, 'gpio': {}, 'inmux': {},
                 'pll': {}, 'spim4': {}, 'tlm': {}, 'tmr1': {}, 'tsm': {}, 'uart1': {}, 'uart2': {}, 'memory': {}}
    for address in errors.keys():
        lines_out[blocks_addresses[address]][address] = errors[address]

    for block in lines_out.keys():
        for address in lines_out[block].keys():
            for error_frame in lines_out[block][address]:
                if error_frame[1][:4] == "F0DA":
                    print(address)
                    exit()

    with open(filename_out, 'w') as file_out:
        json.dump(lines_out, file_out, indent=2)

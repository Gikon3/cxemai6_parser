import json
import operator

from defines import *

# filename_in = "logs_in/1/U_26.09.2019_05-11-54.log"
filename_in = "logs_in/1/U_26.09.2019_05-11-54_correct.log"
filename_out = "logs_out/session_360.log"
filename_reference = "reference.txt"
filename_addresses = "addresses.txt"


def mem_reference(word, word_ref):
    return word_ref if word_ref.upper() != "XXXXXXXX" else "55555555" if word.count("5") > word.upper().count("A") \
        else "aaaaaaaa"


with open(filename_addresses, 'r') as file_addr:
    blocks_addresses = json.load(file_addr)

with open(filename_reference, 'r') as file_ref:
    reference = json.load(file_ref)

with open(filename_in, 'r') as file_in:
    lines_in = file_in.readlines()

# long_lines = []
# for i, line in enumerate(lines_in):
#     if len(line) != 36:
#         print(i + 1)

# for i in long_lines:
#     lines_in[i] = "{0:s}\n{1:s} {2:s}".format(lines_in[i][0:35], "_" * 26, lines_in[i][35:])

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

# ALRM_TMR worked
count = 0
alrm = []
while True:
    try:
        if lines_in[count][27:35] == COM_ALRM_TMR:
            alrm.append(lines_in[count][:26])
            # lines_in.pop(count)
            count += 1

        else:
            count += 1

    except IndexError:
        break

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

# main parse
count = 0
errors = {}
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
                        or lines_in[count + 1][27:35] == COM_ALRM_TMR \
                        or lines_in[count][27:35] == COM_UNRESET_DEVICE \
                        or lines_in[count + 1][27:35] == COM_UNRESET_DEVICE:
                    count += 1
                    break
                if lines_in[count][27:35] not in errors.keys():
                    errors[lines_in[count][27:35]] = []
                if errors_count < number_errors:
                    reference_xor_word = "{0:032b}".format(operator.xor(
                        int(lines_in[count + 1][27:35], 16),
                        int(mem_reference(lines_in[count + 1][27:35],
                                          reference[lines_in[count][27:35]]), 16)))
                    errors[lines_in[count][27:35]].append([lines_in[count][:26], lines_in[count + 1][27:35],
                                                           reference[lines_in[count][27:35]], reference_xor_word])
                    count += 2

        else:
            count += 1

    except IndexError:
        break

lines_out = {'alrm_tmr': [], 'channels': [], 'fts': [], 'gpio': [], 'inmux': [], 'pll': [], 'spim4': [], 'tlm': [],
             'tmr1': [], 'tsm': [], 'uart1': [], 'uart2': [], 'memory': []}
for address in errors.keys():
    lines_out[blocks_addresses[address]].append(errors[address])

with open(filename_out, 'w') as file_out:
    json.dump(lines_out, file_out, indent=2)

import os
import json
import operator

from defines import *

filename_in_list = ["logs_in/session_184/temp/sum_184_alignment.log"]

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
# main parse
    count = 0
    errors = {}
    repeat_packages = []
    memory_failure_coord_package = []
    memory_failure_coord_package_list = []
    while True:
        try:
            if lines_in[count][27:35] in blocks_addresses:
                if blocks_addresses[lines_in[count][27:35]] == "memory":
                    reference_xor_word = "{0:032b}".format(operator.xor(
                        int(lines_in[count + 1][27:35], 16),
                        int(mem_reference(lines_in[count + 1][27:35],
                                          reference[lines_in[count][27:35]]), 16)))

                    if lines_in[count][27:35] not in errors.keys():
                        errors[lines_in[count][27:35]] = []

                    errors[lines_in[count][27:35]].append([lines_in[count][:26],
                                                           lines_in[count + 1][27:35],
                                                           reference[lines_in[count][27:35]],
                                                           reference_xor_word])

                    for i, symbol in enumerate(reference_xor_word[::-1]):
                        if symbol == "1":
                            address_bin = "{0:032b}".format(int(lines_in[count][27:35], 16))
                            memory_failure_coord_package.append(
                                [8 * i + int(address_bin[-5:-2], 2) + 1,
                                 int(address_bin[-6:-5] + address_bin[-22:-6], 2)])

            count += 2

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
            for i, error_frame in enumerate(lines_parse[block][address]):
                if error_frame[1][:4] == "F0DA":
                    print(address)
                    lines_parse[block][address].pop()
                    # exit("Opcode in value")

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
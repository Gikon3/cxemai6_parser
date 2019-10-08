import os
import json

filename_in_list = ["logs_out/session_360/session_360_config.log",
                    "logs_out/session_361/session_361_config.log",
                    "logs_out/session_362/session_362_config.log",
                    "logs_out/session_410/session_410_config.log",
                    "logs_out/session_410/session_410_config.log",
                    "logs_out/session_411/session_411_config.log"]

# lines_out = {'alrm_tmr': {}, 'channels_config': {}, 'channels_accumulate': {}, 'fts': {}, 'gpio': {}, 'inmux': {},
# #              'pll': {}, 'spim4': {}, 'tlm': {}, 'tmr1': {}, 'tsm': {}, 'uart1': {}, 'uart2': {}, 'memory': {}}
lines_out = {'alrm_tmr': {}, 'channels': {}, 'fts': {}, 'gpio': {}, 'inmux': {},
             'pll': {}, 'spim4': {}, 'tlm': {}, 'tmr1': {}, 'tsm': {}, 'uart1': {}, 'uart2': {}, 'memory': {}}

for filename_in in filename_in_list:
    print("Calculate", filename_in)
    filename_out = "number_errors/{0:s}_number_errors.txt".format(
        os.path.splitext(os.path.split(filename_in)[1])[-2][:-7])

    with open(filename_in, 'r') as file_in:
        errors_dict = json.load(file_in)

    for module in errors_dict:
        for address in errors_dict[module]:
            lines_out[module][address] = sum([int(xor[3].count("1")) for xor in errors_dict[module][address]])

    errors_all = {}
    for module in lines_out:
        errors_all[module] = sum([lines_out[module][address] for address in lines_out[module]])

    with open(filename_out, 'w') as file_out:
        file_out.write(filename_in + "\n")
        json.dump(lines_out, file_out, indent=2)
        file_out.write("\n")
        json.dump(errors_all, file_out, indent=2)

import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import colors
import os
import json

filename_coord_list = ["logs_out/session_143/session_143_memory_failure_coord_map.log",
                       "logs_out/session_144/session_144_memory_failure_coord_map.log",
                       "logs_out/session_145/session_145_memory_failure_coord_map.log",
                       "logs_out/session_146/session_146_memory_failure_coord_map.log",
                       "logs_out/session_147/session_147_memory_failure_coord_map.log",
                       "logs_out/session_148/session_148_memory_failure_coord_map.log",
                       "logs_out/session_149/session_149_memory_failure_coord_map.log",
                       "logs_out/session_150/session_150_memory_failure_coord_map.log",
                       "logs_out/session_151/session_151_memory_failure_coord_map.log"]

for filename_coord in filename_coord_list:
    print("Calculate", filename_coord)

    memory_map = np.zeros((4096, 32 * 8))
    with open(filename_coord, 'r') as file_coord:
        coord = (pair[1:-2].split(',') for pair in file_coord)
        coord = ([int(pair[0]), int(pair[1])] for pair in coord)

        for pair in coord:
            memory_map[
                int("{0:032b}".format(pair[1])[16:], 2) + (int("{0:032b}".format(pair[1])[15:16], 2) - 1) * 2048 - 1,
                pair[0] - 1] += 1

    plt.imshow(memory_map)
    name = "images/{0:s}.png".format(os.path.split(filename_coord)[1][:-29])
    plt.savefig(name, interpolation='none', format='png', dpi=2000)

# with open("test.log", 'w') as f_test:
#     f_test.writelines([str(l) + "\n" for l in memory_map])

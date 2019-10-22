import numpy as np
import matplotlib.pyplot as plt
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

    with open(filename_coord, 'r') as file_coord:
        pairs = ((json.loads(pair)[0], json.loads(pair)[1]) for pair in file_coord.readlines())
        coord = ([pair[0] - 1, int(
            "{0:3s}{1:1s}{2:8s}".format("{0:017b}".format(pair[1] - 1)[-11:-8],
                                        "{0:017b}".format(pair[1] - 1)[-17:-16],
                                        "{0:017b}".format(pair[1] - 1)[-8:]), 2)] for pair in pairs)

    memory_map = np.zeros((512 * 8, 32 * 8))
    for pair in coord:
        memory_map[pair[1], pair[0]] = + 1

    fig, ax = plt.subplots()
    ax.matshow(memory_map)
    # ax.grid(color='w', linestyle=':', linewidth=1)
    # ax.set_xticks(np.arange(-.5, 512, 1))
    # ax.set_yticks(np.arange(-.5, 2048, 1))
    # ax.set_xticklabels(np.arange(0, 512, 1))
    # ax.set_yticklabels(np.arange(0, 2048, 1))
    # for i, j in zip(*memory_map.nonzero()):
    #     ax.text(j, i, memory_map[i, j], color='white', ha='center', va='center', fontsize=8)

    # ax.set_xticks(np.arange(-.5, 256, 256))
    # ax.set_yticks(np.arange(-.5, 2048, 512))

    fig.suptitle("Map memory", fontsize=16)

    # plt.show()
    filename_png = "images/{0:s}.png".format(os.path.split(filename_coord)[1][:-29])
    plt.savefig(filename_png, interpolation='none', format='png', dpi=2000)

    for i in range(8):
        ax.matshow(memory_map[512 * i:512 * (i + 1), :])
        filename_png = "images/{0:s}_{1:d}.png".format(os.path.split(filename_coord)[1][:-29], i)
        plt.savefig(filename_png, interpolation='none', format='png', dpi=1000)

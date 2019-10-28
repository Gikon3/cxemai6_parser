sigma_list = [7.93E-9, 5.37E-9, 6.91E-9, 4.95E-9, 3.78E-9, 6.86E-9, 5.95E-9, 1.18E-8, 1.10E-8]
time_list = [683, 662, 429, 392, 285, 95, 344, 388, 454]
M = 2500
w = 32
c = 7

filename_interval_irq_mem_list = ["logs_out/session_143/session_143_time_interval_irq_mem.log",
                                  "logs_out/session_144/session_144_time_interval_irq_mem.log",
                                  "logs_out/session_145/session_145_time_interval_irq_mem.log",
                                  "logs_out/session_146/session_146_time_interval_irq_mem.log",
                                  "logs_out/session_147/session_147_time_interval_irq_mem.log",
                                  "logs_out/session_148/session_148_time_interval_irq_mem.log",
                                  "logs_out/session_149/session_149_time_interval_irq_mem.log",
                                  "logs_out/session_150/session_150_time_interval_irq_mem.log",
                                  "logs_out/session_151/session_151_time_interval_irq_mem.log"]
filename_interval_unreset_list = ["logs_out/session_143/session_143_time_interval_reset.log",
                                  "logs_out/session_144/session_144_time_interval_reset.log",
                                  "logs_out/session_145/session_145_time_interval_reset.log",
                                  "logs_out/session_146/session_146_time_interval_reset.log",
                                  "logs_out/session_147/session_147_time_interval_reset.log",
                                  "logs_out/session_148/session_148_time_interval_reset.log",
                                  "logs_out/session_149/session_149_time_interval_reset.log",
                                  "logs_out/session_150/session_150_time_interval_reset.log",
                                  "logs_out/session_151/session_151_time_interval_reset.log"]


T_list = []
tmp_list = []
for filename_irq_mem, filename_unreset in zip(filename_interval_irq_mem_list, filename_interval_unreset_list):
    with open(filename_irq_mem, 'r') as file_irq_mem:
        line_list = [line[:-1] for line in file_irq_mem.readlines()]
        average_irq_mem = float(line_list[-1][10:])
        # tmp_list = [float(num) for num in line_list[:-1]]
        # average_irq_mem = max(tmp_list)

    with open(filename_unreset, 'r') as file_unreset:
        line_list = [line[:-1] for line in file_unreset.readlines()]
        average_unreset = float(line_list[-1][10:])
        # tmp_list = [float(num) for num in line_list[:-1]]
        # average_unreset = max(tmp_list)

    T_list.append((average_irq_mem + average_unreset) / 2)
    # T_list.append(max(average_irq_mem, average_unreset))

session = 143
for sigma, T, time in zip(sigma_list, T_list, time_list):
    lmbd = sigma * M * (w + c) / time
    # print(lmbd)
    mttf_left = 2 / (M * T * lmbd ** 2 * (w + c) ** 2) - T
    mttf_right = 2 / (M * T * lmbd ** 2 * (w + c) ** 2)
    print(session, "{0:5.3e} < MTTF < {1:5.3e}".format(mttf_left, mttf_right))
    session += 1

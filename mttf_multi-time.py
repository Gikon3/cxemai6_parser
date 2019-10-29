import math
import numpy as np
import matplotlib.pyplot as plt
import re

sigma_list = [5.79E-9, 5.02E-9, 3.86E-9, 1.06E-9, 3.02E-9, 3.14E-9, 7.93E-9, 5.37E-9, 6.91E-9, 4.95E-9, 3.78E-9,
              6.86E-9, 5.95E-9, 1.18E-8, 1.10E-8]
# session            360  361  362  409  410  411  143  144  145  146  147  148  149  150  151
flux_density_list = [254, 384, 470, 514, 343, 559, 278, 390, 444, 496, 266, 281, 555, 505, 410]
#                   [ 10, 300,  10,  10, 300,  10,  10, 300, 300,  10,  10,  10,  10,  10,  10]
time_session_list = [821, 657, 364, 1329, 1250, 651, 683, 662, 429, 392, 285, 95, 344, 388, 454]
M = 1500
w = 32
c = 7

session_list = [360, 361, 362, 409, 410, 411, 143, 144, 145, 146, 147, 148, 149, 150, 151]
filename_interval_unreset_list = ["logs_out/session_360/session_360_time_interval_reset.log",
                                  "logs_out/session_361/session_361_time_interval_reset.log",
                                  "logs_out/session_362/session_362_time_interval_reset.log",
                                  "logs_out/session_409/session_409_time_interval_reset.log",
                                  "logs_out/session_410/session_410_time_interval_reset.log",
                                  "logs_out/session_411/session_411_time_interval_reset.log",
                                  "logs_out/session_143/session_143_time_interval_reset.log",
                                  "logs_out/session_144/session_144_time_interval_reset.log",
                                  "logs_out/session_145/session_145_time_interval_reset.log",
                                  "logs_out/session_146/session_146_time_interval_reset.log",
                                  "logs_out/session_147/session_147_time_interval_reset.log",
                                  "logs_out/session_148/session_148_time_interval_reset.log",
                                  "logs_out/session_149/session_149_time_interval_reset.log",
                                  "logs_out/session_150/session_150_time_interval_reset.log",
                                  "logs_out/session_151/session_151_time_interval_reset.log"]

fig, ax = plt.subplots()
ax.grid(color='black', linestyle=':', linewidth=1)
ax.set_xticks(np.arange(0, 1400, 100))
ax.set_yticks(np.arange(0.91, 1.01, 0.01))
ax.set_xlabel("Time")
ax.set_ylabel("R(t)")

time_unreset_list = []
for filename_unreset, sigma, flux_density, time_session, session in zip(filename_interval_unreset_list, sigma_list,
                                                                        flux_density_list, time_session_list,
                                                                        session_list):
    with open(filename_unreset, 'r') as file_unreset:
        line_list = [line[:-1] for line in file_unreset.readlines()]
        time_unreset_list = (float(line) for line in line_list[:-1])
        average_unreset = float(line_list[-1][10:-1])
        del line_list

    MTTF = 0
    R_all = 1
    build = []
    build_lite = []
    T_total = 0
    for i, T in enumerate(time_unreset_list):
        # lmbd = sigma * M * (w + c) / time_session
        lmbd = sigma * flux_density

        for time in np.arange(0, T, 0.01):
            build.append(
                [T_total + time, math.exp(-lmbd * M * (w + c) * time) * (1 + lmbd * (w + c) * time) ** M * R_all])
        T_total += T

        R = math.exp(-lmbd * M * (w + c) * T) * (1 + lmbd * (w + c) * T) ** M
        MTTF += T * R ** (i + 1)
        R_all *= R
        build_lite.append([T_total, R_all])

    print("{0:d} {1:17.15f} {2:17.15f}".format(session, R_all, MTTF))

    plt.plot([pair[0] for pair in build], [pair[1] for pair in build], label=session)

    with open(f"R_t/w_{session}.log", 'w') as file_build:
        file_build.write(re.sub(']', '}', re.sub('\[', '{', str(build_lite))))

    session += 1

ax.legend(loc=u'lower right', frameon=True)
plt.show()

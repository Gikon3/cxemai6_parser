import os

# filename_in_list = ["logs_in/session_361/U_26.09.2019_06-56-58.log",
#                     "logs_in/session_362/U_26.09.2019_07-18-06.log",
filename_in_list = ["logs_in/session_409/summary_409.log",
                    "logs_in/session_410/U_28.09.2019_23-41-46.log",
                    "logs_in/session_411/U_29.09.2019_00-21-12.log"]

for filename_in in filename_in_list:
    filename_out = "{0:s}/temp/{1:s}_alignment.log".format(os.path.split(filename_in)[0],
                                                           os.path.splitext(filename_in)[0].split('/')[-1])

    with open(filename_in, 'r') as file_in:
        lines_in = file_in.readlines()

    long_lines = []
    for i, line in enumerate(lines_in):
        if len(line) != 36:
            long_lines.append(i)

    for i in long_lines:
        lines_in[i] = "{0:s}\n{1:s} {2:s}".format(lines_in[i][0:35], "_" * 26, lines_in[i][35:])

    with open(filename_out, 'w') as file_out:
        file_out.writelines(lines_in)

    with open(filename_out, 'r') as file_out:
        for i, line in enumerate(file_out.readlines()):
            if len(line) != 36:
                print(i + 1)

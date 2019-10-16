import os

filename_in_list = ["logs_in/session_184/sum_184.log",
                    "logs_in/session_186/U_18.09.2019_23-39-09_parse.log"]
# filename_in_list = ["logs_in/session_360/U_26.09.2019_05-11-54.log",
#                     "logs_in/session_361/U_26.09.2019_06-56-58.log",
#                     "logs_in/session_362/U_26.09.2019_07-18-06.log",
#                     "logs_in/session_409/summary_409_death.log",
#                     "logs_in/session_410/U_28.09.2019_23-41-46.log",
#                     "logs_in/session_411/U_29.09.2019_00-21-12.log"]
filename_addresses = "technical_info/addresses.txt"

# alignment packages
print("Alignment:")
filename_alignment = []
for filename_in in filename_in_list:
    print("  Calculate", filename_in)
    filename_out = "{0:s}/temp/{1:s}_alignment.log".format(os.path.split(filename_in)[0],
                                                           os.path.splitext(filename_in)[0].split('/')[-1])
    filename_alignment.append(filename_out)

    with open(filename_in, 'r') as file_in:
        lines_in = file_in.readlines()

    long_lines = []
    for i, line in enumerate(lines_in):
        if len(line) != 36:
            long_lines.append(i)

    for i in long_lines:
        if len(lines_in[i]) > 36:
            lines_in[i] = "{0:s}\n{1:8s} {2:8s}\n".format(lines_in[i][:35], lines_in[i + 1][:26], lines_in[i][35:-1])
        else:
            lines_in[i] = "{0:s} {1:<8s}\n".format(lines_in[i][:26], lines_in[i][27:-1])

    with open(filename_out, 'w') as file_out:
        file_out.writelines(lines_in)

    with open(filename_out, 'r') as file_out:
        for i, line in enumerate(file_out.readlines()):
            if len(line) != 36:
                print(i + 1)

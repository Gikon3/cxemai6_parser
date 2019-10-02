# filename_in = "logs_in/session_361/U_26.09.2019_06-56-58.log"
# filename_out = "logs_in/session_361/U_26.09.2019_06-56-58_correct.log"

filename_in = "logs_in/session_362/U_26.09.2019_07-18-06.log"
filename_out = "logs_in/session_362/U_26.09.2019_07-18-06_correct.log"


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

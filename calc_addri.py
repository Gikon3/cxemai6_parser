import json
import matplotlib.pyplot as plt

filename_in = "technical_info/haddri.txt"
filename_out = "technical_info/haddri_hist.txt"

print("Calculate", filename_in)

distribution = {}
with open(filename_in, 'r') as file_in:
    address_iter = (line[:-1] for line in file_in.readlines())

    for address in address_iter:
        if hex(int(address, 16)) not in distribution:
            distribution[hex(int(address, 16))] = 1
        else:
            distribution[hex(int(address, 16))] += 1

with open(filename_out, 'w') as file_out:
    json.dump(distribution, file_out, indent=2)

fig = plt.figure()
plt.title('HADDRI Histogram')

ax = plt.axes()
ax.yaxis.grid(True, zorder=1)

plt.bar(distribution.keys(), distribution.values(), color='red')
fig.autofmt_xdate(rotation=90)

plt.show()

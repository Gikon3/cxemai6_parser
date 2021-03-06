import json

filename_in = "technical_info/reference_generate.txt"
filename_reference = "technical_info/reference.txt"
filename_addresses = "technical_info/addresses.txt"

with open(filename_in, 'r') as file_in:
    lines = file_in.readlines()

lines = [line.upper() for line in lines]

blocks_addresses = {}
count = 0
while True:
    try:
        if lines[count][:-1].upper() == "FFFF0001":
            count += 1
            while lines[count][:-1].upper() != "FFFF0002":
                blocks_addresses[lines[count][:-1]] = "alrm_tmr"
                count += 2

        if lines[count][:-1].upper() == "FFFF0002":
            count += 1
            while lines[count][:-1].upper() != "FFFF0012":
                blocks_addresses[lines[count][:-1]] = "channels_config"
                count += 2

        if lines[count][:-1].upper() == "FFFF0012":
            count += 1
            while lines[count][:-1].upper() != "FFFF0003":
                blocks_addresses[lines[count][:-1]] = "channels_accumulate"
                count += 2

        if lines[count][:-1].upper() == "FFFF0003":
            count += 1
            while lines[count][:-1].upper() != "FFFF0004":
                blocks_addresses[lines[count][:-1]] = "fts"
                count += 2

        if lines[count][:-1].upper() == "FFFF0004":
            count += 1
            while lines[count][:-1].upper() != "FFFF0005":
                blocks_addresses[lines[count][:-1]] = "gpio"
                count += 2

        if lines[count][:-1].upper() == "FFFF0005":
            count += 1
            while lines[count][:-1].upper() != "FFFF0006":
                blocks_addresses[lines[count][:-1]] = "inmux"
                count += 2

        if lines[count][:-1].upper() == "FFFF0006":
            count += 1
            while lines[count][:-1].upper() != "FFFF0007":
                blocks_addresses[lines[count][:-1]] = "pll"
                count += 2

        if lines[count][:-1].upper() == "FFFF0007":
            count += 1
            while lines[count][:-1].upper() != "FFFF0008":
                blocks_addresses[lines[count][:-1]] = "spim4"
                count += 2

        if lines[count][:-1].upper() == "FFFF0008":
            count += 1
            while lines[count][:-1].upper() != "FFFF0009":
                blocks_addresses[lines[count][:-1]] = "tlm"
                count += 2

        if lines[count][:-1].upper() == "FFFF0009":
            count += 1
            while lines[count][:-1].upper() != "FFFF000A":
                blocks_addresses[lines[count][:-1]] = "tmr1"
                count += 2

        if lines[count][:-1].upper() == "FFFF000A":
            count += 1
            while lines[count][:-1].upper() != "FFFF000B":
                blocks_addresses[lines[count][:-1]] = "tsm"
                count += 2

        if lines[count][:-1].upper() == "FFFF000B":
            count += 1
            while lines[count][:-1].upper() != "FFFF000C":
                blocks_addresses[lines[count][:-1]] = "uart1"
                count += 2

        if lines[count][:-1].upper() == "FFFF000C":
            count += 1
            while lines[count][:-1].upper() != "FFFF000D":
                blocks_addresses[lines[count][:-1]] = "uart2"
                count += 2

        if lines[count][:-1].upper() == "FFFF000D":
            count += 1
            while lines[count] != "\n":
                blocks_addresses[lines[count][:-1]] = "memory"
                count += 2

        else:
            print(lines[count][:-1])
            count += 1

    except IndexError:
        break

reference = {}
count = 0
while True:
    try:
        if lines[count][:-1].upper() == "FFFF0001" \
                or lines[count][:-1].upper() == "FFFF0002" \
                or lines[count][:-1].upper() == "FFFF0012" \
                or lines[count][:-1].upper() == "FFFF0003" \
                or lines[count][:-1].upper() == "FFFF0004" \
                or lines[count][:-1].upper() == "FFFF0005" \
                or lines[count][:-1].upper() == "FFFF0006" \
                or lines[count][:-1].upper() == "FFFF0007" \
                or lines[count][:-1].upper() == "FFFF0008" \
                or lines[count][:-1].upper() == "FFFF0009" \
                or lines[count][:-1].upper() == "FFFF000A" \
                or lines[count][:-1].upper() == "FFFF000B" \
                or lines[count][:-1].upper() == "FFFF000C" \
                or lines[count][:-1].upper() == "FFFF000D":
            count += 1
        else:
            reference[lines[count][:-1]] = lines[count + 1][:-1]
            count += 2

    except IndexError:
        break

with open(filename_reference, 'w') as file_out:
    json.dump(reference, file_out, indent=2)

with open(filename_addresses, 'w') as file_out:
    json.dump(blocks_addresses, file_out, indent=2)

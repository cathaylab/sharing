#!/usr/bin/python

import sys

location = int(sys.argv[1])

with open("../dataset/train_sample_{}.csv".format(location), "w") as out_file:
    with open("../dataset/train.csv") as in_file:
        is_header = True
        for line in in_file:
            if is_header:
                out_file.write(line)

                is_header = False
            else:
                info = line.strip().split(",")
                x, y = float(info[1]), float(info[2])

                if x >= float(location) and x < float(location)+2 and y >= float(location) and y < float(location)+2:
                    out_file.write(line)

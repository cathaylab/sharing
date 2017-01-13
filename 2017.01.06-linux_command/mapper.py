#!/usr/bin/env python

import sys

for line in sys.stdin:
    if line.strip().isdigit():
        print "number"
    else:
        print "others"

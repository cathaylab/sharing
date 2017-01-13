#!/usr/bin/env python

import sys

results = {}
for line in sys.stdin:
    carrier = line.strip().split(",")[10].lower().strip('"')
    results.setdefault(carrier, 0)

    results[carrier] += 1

for k, v in sorted(results.items(), key=lambda e: e[1], reverse=True):
    print k, v

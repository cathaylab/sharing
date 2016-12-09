#!/usr/bin/python

import re

rows = {}
with open("friend.txt", "rb") as in_file:
    for line in in_file:
        me, friends = re.split("\s+", line.strip())

        rows.setdefault(me, set())
        for friend in friends.split(","):
            rows[me].add(friend)

for me, friends in rows.items():
    for friend in friends:
        if friend in rows and me in rows[friend]:
            print("{} and {} are friends".format(me, friend))

#! /usr/bin/env python
# coding: utf8

import fileinput

userdict = {}

for line in fileinput.input():
    (username, date, timestamp) = line.split('\t')
    
    # test for existence of key. If not present, create empty dict.
    if not username in userdict:
        userdict[username] = {}
    if not date in userdict[username]:
        userdict[username][date] = 1
    else:
        userdict[username][date] += 1
    
print "\t".join(("username", "date", "count"))

for username in sorted(userdict):
    for date in sorted(userdict[username]):
        print "\t".join((username, date, str(userdict[username][date])))

        
    
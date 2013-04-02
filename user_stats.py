#! /usr/bin/env python
# coding: utf8

"""
Accept a list of usernames and times (one per tweet) and add up totals.

This file takes an arbitrary number of files as input, but can also read
the results of tweet_stats.py on STDIN. 

It adds up the number of tweets per day (using the date field, not the 
timestamp field, which is ignored) for each user.

It outputs tab-separated lines to STDOUT, one for each user/date combination.
The outputted fields:

username, date, count

These are also printed as a header line, making the output suitable as
input to R.
"""

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

        
    
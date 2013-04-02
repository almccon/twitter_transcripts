#! /usr/bin/env python
# coding: utf8

"""
Examine HTML twitter logs and extract username and date for each tweet.

This file takes an arbitrary number of files as input. These files must
be in a format outputted by the process_hootsuite.py script.

This file examines each line and extracts three bits of information:
The username (author of the tweet)
The date (actually this is taken from the filename.
The timestamp of the tweet (could be in one of several different formats)

It then outputs tab-separated lines to STDOUT, one for each tweet, with
no header line. The output is suitable to be fed into the user_stats.py 
script.

Suggested usage: ./tweet_stats.py files | ./user_stats.py > output.tsv
"""

import fileinput
import re

debug = False
#debug = True


# fileinput handles an arbitrary number of files as arguments

for line in fileinput.input():

    if (debug): 
        print line  # debug
    
    # extract the date from the filename

    filename = fileinput.filename()
    p = re.compile('\d\d\d\d-\d\d-\d\d')  
    date = p.search(filename)

    # catch the first twitter handle (the author)
    # for the old-style logs, the first handle is missing the "@"

    p = re.compile('.*?<img.*?>\s*@?(\w+)(\s|<)')  
    handle = p.search(line)

    # match the date, old hootsuite styles (Tue Aug 02 18:08:21 +0000 2011), (11:54 AM Jul 26th, 2011) 
    # or new style (2013-02-05T12:06:09)... or failing that, match (1:03pm)
    # For now, just leave the timestamp in all these different styles... deal with it later
  
    p = re.compile('(\w\w\w \w\w\w \d\d \d\d:\d\d:\d\d \+\d\d\d\d \d\d\d\d)|(\d\d:\d\d \w\w \w\w\w \d?\d\w\w, \d\d\d\d)|(\d\d\d\d-\d\d-\d\d\w\d\d:\d\d:\d\d)|(\d?\d:\d\d(a|p)m)') 
    timestamp = p.search(line)

    if handle and timestamp:
        print "\t".join((handle.group(1), date.group(), timestamp.group()))
    else:
        print "COULDN'T PARSE:", line

    if (debug): 
        print "\n"


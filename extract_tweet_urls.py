#! /usr/bin/env python
# coding: utf8

"""
Extract tweet urls from already-processed twitter transcripts

It prints the urls on STDOUT, one per line.

Suggested usage: ./extract_tweet_urls.py twitter_transcript_2012-10-02.html > twitter_transcript_2013-04-02_urls.html
"""

import fileinput
import re

debug = False
#debug = True

p = re.compile('http://twitter.com/.*?/status/[0-9]*')

for line in fileinput.input():
    # I should probably move all these compile stmts outside the loop

    if (debug): 
        print line  # debug

    # grab twitter urls:
    #line = p.search('http://twitter.com/.*?/status/[0-9]*', line)
    match = p.findall(line)
    
    # TODO: if more than one match is found, should raise an error
    print match[0]
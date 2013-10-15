#! /usr/bin/env python
# coding: utf8

"""
Process a set of tweets copied (in HTML) from twitter.com.

This file reads from STDIN a copy-and-pasted file extracted from twitter.com.

This script reverses the order of the lines, so the earliest tweets
come first. It also removes any duplicated lines (the result of RTs)

It prints the result on STDOUT.

Suggested usage: cat twitter_transcript_2013-04-02.html | ./process_twitter_com.py > twitter_transcript_2013-04-02rev.html

I still recommend you check the output to look for any errors in the
conversion process (particularly with character encodings), or manually 
delete irrelevant tweets.

TODO: reorder the tweets according to timestamp.

NOTE: this code is a total messy hack and probably won't work when I try using it again.

"""

import sys
import re

debug = False
#debug = True
data = sys.stdin.read() #read (not readline) will suck up everything


string = data

p = re.compile('\n')
string = p.sub('', string)

p = re.compile('<div class="stream-item-header">')
lines = p.split(string)

lines.reverse() # reverses in place

# Create a dictionary of lines to track duplicates.
# We have to do it this way because duplicates may not be adjacent to one another.
# Duplicates occur because of the way hootsuite currently displays RTs 
linedict = {} 

for line in lines:
    # I should probably move all these compile stmts outside the loop

#    if (debug): 
#        print line  # debug

    p = re.compile('tweet-text')
    if not p.search(line):
        if debug:
            print "skipping"
        next

    # Replace tabs with spaces 
    p = re.compile('\t')
    line = p.sub(' ', line)

    # clean up the stupid "..." symbol
    #p = re.compile(u"\xe2") 
    p = re.compile('…') 
    line = p.sub('...', line)

    p = re.compile('“') 
    line = p.sub('"', line)

    p = re.compile('”') 
    line = p.sub('"', line)

    p = re.compile('’') 
    line = p.sub("'", line)

    p = re.compile('‘') 
    line = p.sub("'", line)

    p = re.compile('^ *') # 
    line = p.sub('<br clear=all><p>', line)

    p = re.compile('<img class="avatar js-action-profile-avatar" src') # 
    line = p.sub('<img height="48px" width="48px" align="left" src', line)

    p = re.compile('<strong class="fullname.*?-name">') # .*? is non-greedy version of .*
    line = p.sub('', line)

    p = re.compile('<s>')
    line = p.sub('', line)

    p = re.compile('</s>')
    line = p.sub('', line)

    p = re.compile('<strong>')
    line = p.sub('', line)

    p = re.compile('</strong>')
    line = p.sub('', line)

    p = re.compile('</div>')
    line = p.sub('', line)

    p = re.compile('<div class="stream-item-footer".*') # .*? is non-greedy
    line = p.sub('', line)

    p = re.compile('href="/') # fix relative links
    line = p.sub('href="http://twitter.com/', line)

    #TODO: fix this
#    p = re.compile('</b> *</a>')
#    line = p.sub('</b></a>', line)

    p = re.compile('<small class="time">')
    line = p.sub('', line)

    p = re.compile('</small>')
    line = p.sub('', line)

    p = re.compile('class="tweet-timestamp.*?title="') # .*? is non-greedy
    line = p.sub('>', line)

    p = re.compile('" ?><span class="_timestamp.*?data-long-form="true">\d\d? \w\w\w') # .*? is non-greedy
    line = p.sub('', line)

    p = re.compile('<span .*?>') # .*? is non-greedy
    line = p.sub('', line)

    p = re.compile('</span>')
    line = p.sub('', line)

    p = re.compile('<p .*?>') # .*? is non-greedy
    line = p.sub('', line)

    p = re.compile('</p>')
    line = p.sub('', line)

#    p = re.compile('<a href.*<span class="details-icon') # .*? is non-greedy
#    line = p.sub('<span class="details-icon', line)
#    p = re.compile('<a href.*<span class="details-icon') # .*? is non-greedy
#    line = p.sub('<span class="details-icon', line)

    # now to remove the </a> after people's names
#    p = re.compile('>\s+(\S+)<\/a>\s\s\s') # + requires at least one is non-greedy
#    line = p.sub('> @\\1', line, 1) # The trailing 1 stops this after the 1st sub

    # Also do this, to remove </a> after handles and hashtags in body of tweets:
#    p = re.compile('([@#]\S*)<\/a>') 
#    line = p.sub('\\1', line)

    # remove junk from the end:
#    p = re.compile('<\/p>.*<\/div>') 
#    line = p.sub('', line)

    # remove the "via" stuff:
#    p = re.compile('via\s\s\s\s.*?a>') 
#    line = p.sub('</a>', line)
  
    # remove <a class="_previewLink...  
#    p = re.compile('<\/a><a href.*?class="_previewLink.*?><\/a>') 
#    line = p.sub('</a>', line)
   
    # Remove repeated spaces (if there are two or more, replace with two)
    p = re.compile('\s+')
    line = p.sub(' ', line)

    p = re.compile(' @<b>')
    line = p.sub('@', line)

    p = re.compile('</b> </a>')
    line = p.sub('</a>', line)

    p = re.compile('<b>')
    line = p.sub('', line)

    p = re.compile('</b>')
    line = p.sub('', line)



    if line in linedict:
        # We have seen an identical line. Do not print.
        linedict[line] += 1
    else:
        print line
        linedict[line] = 1

    if (debug): 
        print "\n"
        print "\n"
        print "\n"


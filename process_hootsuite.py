#! /usr/bin/env python
# coding: utf8

import sys
import re

debug = False
#debug = True
data = sys.stdin.read() #read (not readline) will suck up everything


string = data

p = re.compile('\n')
string = p.sub('', string)

p = re.compile('<div id')
lines = p.split(string)

lines.reverse() # reverses in place

for line in lines:
  # I should probably move all these compile stmts outside the loop

  if (debug): 
    print line  # debug

  p = re.compile('lazysrc')
  line = p.sub('src', line)

  p = re.compile(' class="networkAvatar.*?"') # .*? is non-greedy version of .*
  line = p.sub('', line)

  p = re.compile('^.*<img src') # ^ to match beginning of string
  line = p.sub('<br clear=all><p><img height="48px" align="left" src', line)

  p = re.compile('<p class.*?>') # .*? is non-greedy version of .*
  line = p.sub('', line)

  p = re.compile('<a href="#" class="_user.*?>') # .*? is non-greedy
  line = p.sub('', line)

  p = re.compile('<a href="#" class="_quick.*?>') # .*? is non-greedy
  line = p.sub('', line)

  # now to remove the </a> after people's names
  p = re.compile('>\s+(\S+)<\/a>\s\s\s') # + requires at least one is non-greedy
  line = p.sub('> @\\1', line, 1) # The trailing 1 stops this after the 1st sub

  # Also do this, to remove </a> after handles and hashtags in body of tweets:
  p = re.compile('([@#]\S*)<\/a>') 
  line = p.sub('\\1', line)

  # remove junk from the end:
  p = re.compile('<\/p>.*<\/div>') 
  line = p.sub('', line)

  # remove the "via" stuff:
  p = re.compile('via\s\s\s\s.*?a>') 
  line = p.sub('</a>', line)

  # remove <a class="_previewLink...  
  p = re.compile('<\/a><a href.*?class="_previewLink.*?><\/a>') 
  line = p.sub('</a>', line)

  # clean up the stupid "..." symbol
  #p = re.compile(u"\xe2") 
  p = re.compile('…') 
  line = p.sub('...', line)

  print line

  if (debug): 
    print "\n"


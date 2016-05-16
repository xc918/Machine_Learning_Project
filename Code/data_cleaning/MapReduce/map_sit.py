#!/usr/bin/env python

# This is the third part of the MapReduce process. We add features whether two judges 
# in the circut has been sitting together before and their dissent rate according to 
# their previous records.  
import sys

for line in sys.stdin:
    line = line.strip()
    info = line.split(',')
    if info[0][0] == 'X':
        print '%s\t%d,%s'%(info[-1], 0, ','.join(info[:-1]))
    else:
        print '%s\t%d,%s'%(info[0], 1, ','.join(info[1:]))

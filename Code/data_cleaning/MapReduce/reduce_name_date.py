#!/usr/bin/env python

# This is the second part of the MapReduce process. We will reduce the result from step 1 
# to the following format: [name of two judges in each case][dates they sit together] 

import sys

current_key = None
key = None
date = []

for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t')
    if current_key == key:
        date.append(value)
    else:
        if len(date) > 0:
            print '%s,%s' %(current_key,';'.join(date))
        current_key = key
        date = []
        date.append(value)
print '%s,%s' %(current_key,';'.join(date))
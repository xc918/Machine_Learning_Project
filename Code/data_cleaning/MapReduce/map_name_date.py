#!/usr/bin/env python

# This is the second part of the MapReduce process. We will reduce the result from step 1 
# to the following format: [name of two judges in each case][dates they sit together] 

import sys

for line in sys.stdin:
    line = line.strip()
    info = line.split(',')
    print '%s\t%s'%(info[-1],str(tuple([info[1],info[-2]])))

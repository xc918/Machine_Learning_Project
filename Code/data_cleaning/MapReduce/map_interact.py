#!/usr/bin/env python

# This is the first part of the MapReduce process. We merged (i) votelevel data containing information about 
# each case and three judges and (ii) target variable indicating whether two judges agree with each other.
# After the this step, each entry of the data should look like: 
# [case info][J1 info][J2 info][J1J2 cross info][dissent_dummy]
import sys

for line in sys.stdin:
    line = line.strip()
    info = line.split(',')
    if info[0] != 'caseid':
    	if len(info)==4:
    		print (info[0] + '\t' + '2,' + ','.join(info[1:]))
    	else:
    		#case info
	    	print (info[0]+'\t'+'1,'+','.join(info[1:21]))
	    	#judge info
	    	print (info[0]+'\t'+'0,'+','.join(info[21:]))


#!/usr/bin/env python

# This is the third part of the MapReduce process. We add features whether two judges 
# in the circut has been sitting together before and their dissent rate according to 
# their previous records.  

import sys
from datetime import datetime
from ast import literal_eval as make_tuple

current_key = None
key = None
dates = []
cases = []
case_date=[]
sit = ['0','0','0','0']
dissent_rate = 0.0


for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t')
    if current_key == key:
        if value[0] == '0':
            cases.append(value[2:])
            case_date.append(value[2:].split(',')[1])
        else:
            alldates = [make_tuple(i) for i in value[2:].split(';')] 
            dates = [i[0] for i in alldates]   
            dissent = [int(i[1]) for i in alldates]   
    else:
        if case_date:
            for date in case_date:
                if dates.index(date) > 0:
                    previous = dates[dates.index(date)-1]
                    previous_dt = datetime.strptime(previous[:10],'%Y-%m-%d')
                    date_dt = datetime.strptime(date[:10],'%Y-%m-%d')
                    if (date_dt - previous_dt).days < 360:
                        if (date_dt - previous_dt).days < 180:
                            if (date_dt - previous_dt).days < 90:
                                sit = ['1','1','1','1']
                            else:
                                sit = ['0','1','1','1']
                        else:
                            sit = ['0','0','1','1']
                    else:
                        ['0','0','0','1']
                    dissent_rate= sum(dissent[:dates.index(date)])/float(len(dissent[:dates.index(date)]))
                else:
                    sit = ['0','0','0','0']
                    dissent_rate=0.0
                
                print '%s,%s,%.6f' %(cases[case_date.index(date)],','.join(sit), dissent_rate)

        current_key = key
        dates = []
        cases = []
        case_date=[]
        sit = ['0','0','0','0']
        dissent_rate = 0.0
        if value[0] == '0':
            cases.append(value[2:])
            case_date.append(value[2:].split(',')[1])
        else:
            alldates = [make_tuple(i) for i in value[2:].split(';')] 
            dates = [i[0] for i in alldates]   
            dissent = [int(i[1]) for i in alldates] 

if case_date:
    for date in case_date:
        if dates.index(date) > 0:
            previous = dates[dates.index(date)-1]
            previous_dt = datetime.strptime(previous[:10],'%Y-%m-%d')
            date_dt = datetime.strptime(date[:10],'%Y-%m-%d')
            if (date_dt - previous_dt).days < 360:
                if (date_dt - previous_dt).days < 180:
                    if (date_dt - previous_dt).days < 90:
                        sit = ['1','1','1','1']
                    else:
                        sit = ['0','1','1','1']
                else:
                    sit = ['0','0','1','1']
            else:
                ['0','0','0','1']
            dissent_rate = sum(dissent[:dates.index(date)])/float(len(dissent[:dates.index(date)]))

        else:
            sit = ['0','0','0','0']
            dissent_rate = 0.0
        print '%s,%s,%.6f' %(cases[case_date.index(date)],','.join(sit), dissent_rate)

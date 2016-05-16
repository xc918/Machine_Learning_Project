#!/usr/bin/env python

# This is the first part of the MapReduce process. We merged (i) votelevel data containing information about 
# each case and three judges and (ii) target variable indicating whether two judges agree with each other.
# After the this step, each entry of the data should look like: 
# [case info][J1 info][J2 info][J1J2 cross info][dissent_dummy]
import sys

current_key = None
info = dict.fromkeys(['case','1','2','3'], None)
j=[]
cross_terms=[1,2,3,11,17,20,22,23,24,30,32,33,35]
#1: agegroup 2: term 3: birthyear group 11:presidentname 17:lasename_predecessor 20:party 22:gender 
#23: raceorethnicity  24: partyaffiliationofpresident 30:stateofresident 
#32: appres 33:aba 35: unity
school = []

for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t', 1)
    if current_key == key:
        if value[0]=='1':
            info['case'] = value[2:]
        elif value[0]=='2':
            dissent = value[2:].split(',')
        else:
            j_num = value[2]
            info[j_num] = value[4:].split(',')
    else:
        if info['case']:
            try:
                #j1j2
                j=[]
                for i in cross_terms:
                    if info['1'][i]==info['2'][i]:
                        j.append('1')
                    else:
                        j.append('0')

                school = [info['1'][25], info['1'][26], info['2'][25], info['2'][26]] 
                if len(set(school)) == 4:
                    j.append('0')
                else:
                    j.append('1')
                j.append(dissent[0])
                #merge songername
                j.append('&'.join(set([info['1'][0],info['2'][0]])))
                if j[-2] != '-1':
                    print '%s,%s,%s,%s,%s'%(current_key, info['case'], ','.join(info['1']),','.join(info['2']),','.join(j))
                #j1j3
                j=[]
                for i in cross_terms:
                    if info['1'][i]==info['3'][i]:
                        j.append('1')
                    else:
                        j.append('0')
                school = [info['1'][25], info['1'][26], info['3'][25], info['3'][26]] 
                if len(set(school)) == 4:
                    j.append('0')
                else:
                    j.append('1')
                j.append(dissent[1])
                #merge songername
                j.append('&'.join(set([info['1'][0],info['3'][0]])))
                if j[-2] != '-1':
                    print '%s,%s,%s,%s,%s'%(current_key, info['case'], ','.join(info['1']),','.join(info['3']),','.join(j))
                
                #j2j3
                j=[]
                for i in cross_terms:
                    if info['2'][i]==info['3'][i]:
                        j.append('1')
                    else:
                        j.append('0')

                school = [info['2'][25], info['2'][26], info['3'][25], info['3'][26]] 
                if len(set(school)) == 4:
                    j.append('0')
                else:
                    j.append('1')
                j.append(dissent[2])
                #merge songername
                j.append('&'.join(set([info['2'][0],info['3'][0]])))
                if j[-2] != '-1':
                    print '%s,%s,%s,%s,%s'%(current_key, info['case'], ','.join(info['2']), ','.join(info['3']), ','.join(j))
            except TypeError:
                pass

        current_key = key
        info = dict.fromkeys(['case','1','2','3'], None)
        if value[0]=='1':
            info['case'] = value[2:]
        elif value[0]=='2':
            dissent = value[2:].split(',')
        else:
            j_num = value[2]
            info[j_num] = value[4:].split(',')

#j1j2
j=[]
for i in cross_terms:
    if info['1'][i]==info['2'][i]:
        j.append('1')
    else:
        j.append('0')
school = [info['1'][25], info['1'][26], info['2'][25], info['2'][26]] 
if len(set(school)) == 4:
    j.append('0')
else:
    j.append('1')
j.append(dissent[0])
#merge songername
j.append('&'.join(set([info['1'][0],info['2'][0]])))
if j[-2] != '-1':
    print '%s,%s,%s,%s,%s'%(current_key, info['case'], ','.join(info['1']),','.join(info['2']),','.join(j))
#j1j3
j=[]
for i in cross_terms:
    if info['1'][i]==info['3'][i]:
        j.append('1')
    else:
        j.append('0')
school = [info['1'][25], info['1'][26], info['3'][25], info['3'][26]] 
if len(set(school)) == 4:
    j.append('0')
else:
    j.append('1')
j.append(dissent[1])
#merge songername
j.append('&'.join(set([info['1'][0],info['3'][0]])))
if j[-2] != '-1':
    print '%s,%s,%s,%s,%s'%(current_key, info['case'], ','.join(info['1']),','.join(info['3']),','.join(j))
#j2j3
j=[]
for i in cross_terms:
    if info['2'][i]==info['3'][i]:
        j.append('1')
    else:
        j.append('0')
school = [info['2'][25], info['2'][26], info['3'][25], info['3'][26]] 
if len(set(school)) == 4:
    j.append('0')
else:
    j.append('1')
j.append(dissent[2])
#merge songername
j.append('&'.join(set([info['2'][0],info['3'][0]])))
if j[-2] != '-1':
    print '%s,%s,%s,%s,%s'%(current_key, info['case'], ','.join(info['2']),','.join(info['3']),','.join(j))

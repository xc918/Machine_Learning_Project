import pandas as pd
import numpy as np
import pickle

def get_judge1_name(item):

    # split the judges name in a string by '|'
    list_item = list(np.unique([x.upper() for x in item.strip().split('|')]))
    if 'NONE' in list_item:
        list_item.remove('NONE')
    else:
        pass
    if len(list_item) == 0:
        return ['NONE', 'NONE', 'NONE']
    elif len(list_item) == 1:
        return [list_item[0], 'NONE', 'NONE']
    elif len(list_item) == 2:
        return [list_item[0], list_item[1], 'NONE']
    else:
        return [list_item[0], list_item[1], list_item[2]]

def get_judge_name(item):

    list_item = item.strip().split(',')

    return list_item[0]

def get_dissent_judge(data):

    # slice data with only target information
    target = data[['caseid', 'JudgeCONCURRING', 'JudgeDissentingTouse', 'Judgeconcurring', 'JudgeDissenting', 'MultipleDissents','Author','Writer', 'j', 'songername']]

    # 'DISSENTING_JUDGE' contains all judges who dissent
    target['DISSENTING_JUDGE'] = target['Judgeconcurring']+'|'+target['JudgeDissenting']

    target['Dissenting_judge1'] = 'NONE'
    target['Dissenting_judge2'] = 'NONE'
    target['Dissenting_judge3'] = 'NONE'

    # get names of all judges in a case who dissent in a list 
    judges_name = target['DISSENTING_JUDGE'].map(lambda x: get_judge1_name(x))
    
    for i in range(3):
        target['Dissenting_judge'+str(i+1)] = judges_name.map(lambda x: x[i])

    # standardize the name of judges
    target['judge_name'] = target['songername'].map(lambda x: get_judge_name(x))

    return target

def get_dissent_dummy(target):

    case_dict = {}
    case_pro_list = []
    # list the dissent dummy for judge pairs [j1-j2, j1-j3, j2-j3]. Abnormal cases will be included in case_pro_list when an error raises.

    for case in target['caseid'].unique():
    try:
        target_case = target[target['caseid'] == case]
        writer_id = target_case['Writer'].unique()[0]
        judge1_name = target_case['Dissenting_judge1'].unique()[0]
        judge2_name = target_case['Dissenting_judge2'].unique()[0]
        judge3_name = target_case['Dissenting_judge3'].unique()[0]
        judge_list = [judge1_name, judge2_name, judge3_name]
        if writer_id == 0.0:
            if judge1_name == 'NONE':
                new_list = [0,0,0]
            else:
                if judge2_name == 'NONE':
                    j = target_case[target_case['judge_name'] == judge1_name]['j'].values[0]
                    if j == 1:
                        new_list = [1,1,0]
                    elif j == 2:
                        new_list = [1,0,1]
                    else:
                        new_list = [0,1,1]
                else:
                    if judge3_name == 'NONE':
                        j1 = target_case[target_case['judge_name'] == judge1_name]['j'].values[0]
                        j2 = target_case[target_case['judge_name'] == judge2_name]['j']
                        if len(j2) == 0:
                            if j1 == 1:
                                new_list = [1,1,0]
                            elif j1 == 2:
                                new_list = [1,0,1]
                            else:
                                new_list = [0,1,1]
                        else:
                            j = 6 - j1 - j2.values[0]
                            if j == 1:
                                new_list = [1,1,0]
                            elif j == 2:
                                new_list = [1,0,1]
                            else:
                                new_list = [0,1,1]
                    else:
                        new_list = [0,0,0]
        else:
            target_nowriter = target_case[target_case['j'] != int(writer_id)]
            if writer_id == 1.0:
                target_nowriter_1 = target_nowriter[target_nowriter['j'] == 2]['judge_name'].values[0]
                target_nowriter_2 = target_nowriter[target_nowriter['j'] == 3]['judge_name'].values[0]
                if target_nowriter_1 not in judge_list:
                    if target_nowriter_2 not in judge_list:
                        new_list = [0,0,-1]
                    else:
                        new_list = [0,1,-1]
                else:
                    if target_nowriter_2 not in judge_list:
                        new_list = [1,0,-1]
                    else:
                        new_list = [1,1,-1]
            elif writer_id == 2.0:
                target_nowriter_1 = target_nowriter[target_nowriter['j'] == 1]['judge_name'].values[0]
                target_nowriter_2 = target_nowriter[target_nowriter['j'] == 3]['judge_name'].values[0]
                if target_nowriter_1 not in judge_list:
                    if target_nowriter_2 not in judge_list:
                        new_list = [0,-1,0]
                    else:
                        new_list = [0,-1,1]
                else:
                    if target_nowriter_2 not in judge_list:
                        new_list = [1,-1,0]
                    else:
                        new_list = [1,-1,1]
            else:
                target_nowriter_1 = target_nowriter[target_nowriter['j'] == 1]['judge_name'].values[0]
                target_nowriter_2 = target_nowriter[target_nowriter['j'] == 2]['judge_name'].values[0]
                if target_nowriter_1 not in judge_list:
                    if target_nowriter_2 not in judge_list:
                        new_list = [-1,0,0]
                    else:
                        new_list = [-1,0,1]
                else:
                    if target_nowriter_2 not in judge_list:
                        new_list = [-1,1,0]
                    else:
                        new_list = [-1,1,1]  
        case_dict[case] = new_list
    except IndexError:
        case_pro_list.append(case)

    return case_dict, case_pro_list

def main():

    path = './votelevel_cleand.csv'
    data = pd.read_csv(path)

    target = get_dissent_judge(data)

    case_dict, case_pro_list = get_dissent_dummy(target)

if __name__ == '__main__':

    '''
    From the code we will generate a dictionary containing the dissent dummy for each case in a format of [j1-j2, j1-j3, j2-j3].
    Abnormal cases are included in a list. It requires manually modifying the list.
    '''
    main()

    pickle.dump(case_pro_list, open('case_pro_list.p', 'wb'))
    pickle.dump(case_dict, open('case_dict.p', 'wb'))



















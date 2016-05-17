import pandas as pd
import numpy as np
import random
import datetime
import pickle

def merge_mapreduce(data):
    interact_col_names = pickle.load('col_names.p')
    pd.options.display.float_format = '{:,.6f}'.format
    
    data = data.drop(['case_caseid', 'case_date', 'J1_songername', 'J2_songername', 'J1_nameofschool1',
	                      'J1_nameofschool2', 'J2_nameofschool1', 'J2_nameofschool2'], 1)
    data.to_csv('data_mapreduce_clean.csv', index=False)

if __name__ == '__main__':
	
	path = './MapReduce/data_mapreduce.csv'
	data = pd.read_csv(path, names=interact_col_names)


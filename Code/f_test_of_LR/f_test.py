import gc
import pickle
import numpy as np
import time
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics

def get_sum(list1, list2):
    sum = 0
    for i in range(len(list1)):
	sum += pow(list1[i]-list2[i],2)

    return sum

def f_test(data):

    data_train, data_test = train_test_split(data, test_size=0.25)

    f_value_dict = {}

    X_train = data_train.drop('dissent_dummy',1)
    Y_train = data_train['dissent_dummy']
    X_test = data_test.drop('dissent_dummy', 1)
    Y_test = data_test['dissent_dummy']

    del data_train, data_test
    gc.collect()

    lr = LogisticRegression()
    lr.fit(X_train, Y_train)
    predict_array = lr.predict_proba(X_test)[:,1]
        
    n = X_test.shape[0]-1
    m = X_test.shape[1]
    
    std = get_sum(Y_test.tolist(), predict_array.tolist())
    
    del lr 
    gc.collect()

    for column in X_train.columns[:200]:
        
        start_time = time.time()

        X_train_col = X_train.drop(column, 1)
        X_test_col = X_test.drop(column, 1)
        
        lr = LogisticRegression()
        lr.fit(X_train_col, Y_train)
        predict_array_col = lr.predict_proba(X_test_col)[:,1]

        std_col = get_sum(Y_test.tolist(), predict_array_col.tolist())

        f_value = (std_col - std)/(std)*(n-m-1)

        f_value_dict[column] = f_value
    
        print column, f_value_dict[column]
        print (time.time() - start_time)      
    
        del lr, X_train_col, X_test_col
        gc.collect()
            
    pickle.dump(f_value_dict, open('./f_value_dict_part20_604.p', 'wb'))

if __name__ == '__main__':

    path = './0504_normalize_data.csv'
    data = pd.read_csv(path)
    f_test(data)





            


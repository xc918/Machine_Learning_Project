import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, roc_auc_score
from sklearn.preprocessing import normalize, minmax_scale, MinMaxScaler
import matplotlib.pyplot as plt



def load_data(path):
    data = pd.read_csv(path)
    X = data.drop('dissent_dummy',1)
    Y = data['dissent_dummy']
    X_train, X_sample, Y_train, Y_sample = train_test_split(X, Y, test_size=0.2)
    X_train, X_test, Y_train, Y_test = train_test_split(X_sample, Y_sample, test_size=0.25)
    case_names = ['case_MajOpinionWordCount', 'case_MajSelfCertainWords',
               'case_minOpinionWordCount2', 'case_MinSelfCertainWords2',
               'case_ConcurenceWordCount2', 'case_ConcurSelfCertainWords2',
               'case_PossibleTypoInDissenterOrJudge', 'case_RehearingOrPetition',
               'case_ConcurenceMistakenForDissent', 'case_distance',
               'case_lastquarter', 'case_last3','case_Circuit_0', 'case_Circuit_1',
               'case_Circuit_2', 'case_Circuit_3', 'case_Circuit_4',
               'case_Circuit_5', 'case_Circuit_6', 'case_Circuit_7',
               'case_Circuit_8', 'case_Circuit_9', 'case_Circuit_10',
               'case_Circuit_11', 'case_Circuit_12','case_geniss_0.0', 'case_geniss_1.0',
               'case_geniss_2.0', 'case_geniss_3.0', 'case_geniss_4.0',
               'case_geniss_5.0', 'case_geniss_6.0', 'case_geniss_7.0',
               'case_geniss_9.0', 'case_Treat_-1.0', 'case_Treat_0.0',
               'case_Treat_1.0', 'case_Treat_2.0', 'case_Treat_3.0',
               'case_Treat_4.0', 'case_Treat_5.0', 'case_Treat_6.0',
               'case_Treat_7.0', 'case_Treat_8.0', 'case_quartertoelect_1.0',
               'case_quartertoelect_2.0', 'case_quartertoelect_3.0',
               'case_quartertoelect_4.0', 'case_quartertoelect_5.0',
               'case_quartertoelect_6.0', 'case_quartertoelect_7.0',
               'case_quartertoelect_8.0', 'case_quartertoelect_9.0',
               'case_quartertoelect_10.0', 'case_quartertoelect_11.0',
               'case_quartertoelect_12.0', 'case_quartertoelect_13.0',
               'case_quartertoelect_14.0', 'case_quartertoelect_15.0',
               'case_quartertoelect_16.0', 'case_quarter_1.0', 'case_quarter_2.0',
               'case_quarter_3.0', 'case_quarter_4.0', 'case_Circuitjudge_-1.0',
               'case_Circuitjudge_0.0', 'case_Circuitjudge_1.0',
               'case_Circuitjudge_2.0', 'case_Circuitjudge_3.0',
               'case_Circuitjudge_4.0', 'case_Circuitjudge_5.0',
               'case_Circuitjudge_6.0', 'case_Circuitjudge_7.0',
               'case_Circuitjudge_8.0', 'case_Circuitjudge_9.0',
               'case_Circuitjudge_10.0', 'case_Circuitjudge_11.0',
               'case_Circuitjudge_12.0', 'case_Circuitjudge_13.0']
    X_train_case = X_train[case_names]
    X_test_case = X_test[case_names]
    X_train_judge = X_train.drop(case_names,1)
    X_test_judge = X_test.drop(case_names,1)
    return X_train, X_test, Y_train, Y_test, X_train_case, X_test_case, X_train_judge, X_test_judge


def main(path):
    X_train, X_test, Y_train, Y_test, X_train_case, X_test_case, X_train_judge, X_test_judge = load_data(path)

    output_imp = pd.DataFrame(columns=['rf_imp','rf_name','rf_yerr','rf_case_imp','rf_case_name',
                                       'rf_case_yerr','rf_judge_imp','rf_judge_name','rf_judge_yerr'])

    col_names = X_train.columns.values
    col_names_case = X_train_case.columns.values
    col_names_judge = X_train_judge.columns.values

    ytest = pd.DataFrame(Y_test)
    ytest.to_csv('y_test.csv',index=False)

    rf = RandomForestClassifier(n_estimators=500, random_state=123, bootstrap=False).fit(X_train, Y_train)
    rf_case = RandomForestClassifier(n_estimators=200, random_state=123, bootstrap=False).fit(X_train_case,Y_train)
    rf_judge = RandomForestClassifier(n_estimators=500, random_state=123, bootstrap=False).fit(X_train_judge,Y_train)

    importances = rf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    output_imp.rf_name = col_names[indices[:20]]
    output_imp.rf_imp = importances[indices[:20]]
    output_imp.rf_yerr = std[indices[:20]]

    importances = rf_case.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf_case.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    output_imp.rf_case_name = col_names_case[indices[:20]]
    output_imp.rf_case_imp = importances[indices[:20]]
    output_imp.rf_case_yerr = std[indices[:20]]

    importances = rf_judge.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf_judge.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    output_imp.rf_judge_name = col_names_judge[indices[:20]]
    output_imp.rf_judge_imp = importances[indices[:20]]
    output_imp.rf_judge_yerr = std[indices[:20]]

    output_imp.to_csv('importance.csv',index=False)
    lr_l1 = LogisticRegression(penalty='l1', random_state=123).fit(X_train, Y_train)
    lr_l2 = LogisticRegression(penalty='l2', random_state=123).fit(X_train, Y_train)
    nb = GaussianNB().fit(X_train, Y_train)

    pred = [lr_l1.predict_proba(X_test)[:,1], lr_l2.predict_proba(X_test)[:,1],
            rf.predict_proba(X_test)[:,1], rf_case.predict_proba(X_test_case)[:,1],
            rf_judge.predict_proba(X_test_judge)[:,1],nb.predict_proba(X_test)[:,1]]

    labels = ['LR_L1','LR_L2','RF','RF_case','RF_judge','NB']
    output_data = pd.DataFrame(np.array(pred).T, columns = labels)
    output_data.to_csv('output_plot_auc.csv',index=False)


if __name__ == '__main__':

    path = './0504_normalize_data.csv'
    main(path)



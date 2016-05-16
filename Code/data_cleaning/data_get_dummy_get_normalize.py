import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def get_dummy(data):

    list_to_category = ['J2_District_Circuit', 'J2_ResidenceCity', 'J2_appres', 'J2_unityi', 'J2_raceorethnicity', 
                        'J2_district', 'J2_party_Updated', 'J2_Degree1', 'J2_presidentname', 'J2_State', 
                        'J2_senatevoicevote', 'case_Circuit', 'J2_Degree2', 'J2_Degree3', 'J2_Committeeaction', 
                        'J2_placeofbirthstate', 'J2_partyaffiliationofpresident', 'J2_left', 'J2_StateOfResidence', 
                        'J2_aba', 'J2_congresi', 'inter_presidentname', 'case_geniss', 'case_Treat', 'case_quartertoelect', 
                        'case_quarter', 'case_Circuitjudge', 'J1_Term', 'J1_State', 'J1_presidentname', 
                        'J1_senatevoicevote', 'J1_Degree1', 'J1_Degree2', 'J1_Degree3', 'J1_Committeeaction', 
                        'J1_placeofbirthstate', 'J1_party_Updated', 'J1_district', 'J1_raceorethnicity', 
                        'J1_partyaffiliationofpresident', 'J1_District_Circuit', 'J1_pres', 'J1_left', 
                        'J1_StateOfResidence', 'J1_ResidenceCity', 'J1_appres', 'J1_aba', 'J1_congresi', 'J1_unityi', 
                        'J2_Term', 'J1_birthyear', 'J2_birthyear', 'J1_ageon', 'J2_ageon']

    list_to_numerical = ['J2_hrep', 'J2_sdem', 'J2_srep', 'J2_hother', 'J2_sother', 'case_MajOpinionWordCount', 
                         'case_MajSelfCertainWords', 'case_minOpinionWordCount2', 'case_MinSelfCertainWords2', 
                         'case_ConcurenceWordCount2', 'case_ConcurSelfCertainWords2', 'case_distance', 'J1_hdem', 
                         'J1_hrep', 'J1_sdem', 'J1_srep', 'J1_hother', 'J1_sother', 'J2_hdem']

    list_to_delete = ['J1_vicelastnamepredecessor', 'J1_vicefirstnamepredecessor','J2_vicelastnamepredecessor', 
                      'J2_vicefirstnamepredecessor', 'J2_pres', 'case_yearq']


    new_data = data.drop(list_to_delete, 1)

    for column in list_to_category:  
        new_data = pd.merge(new_data, pd.get_dummies(data[column], prefix = column), left_index=True, right_index=True) # convert categorical variables into dummy variables

    new_data = new_data.drop(list_to_category, 1)

    return new_data

def get_normalize(data):

    data_features = data.drop('dissent_dummy', 1)

    min_max_scaler = MinMaxScaler()

    data_minmax = min_max_scaler.fit_transform(data_features)

    data_output = pd.DataFrame(data_minmax, columns = data_features.columns)

    data_output['dissent_dummy'] = data['dissent_dummy'] 

    return data_output

def main():

    data = pd.read_csv('data_mapreduce_clean.csv')

    new_data = get_dummy(data)

    data_output = get_normalize(new_data)

    data_output.to_csv('data_normalize.csv', index = False)

if __name__ == '__main__':
    main()














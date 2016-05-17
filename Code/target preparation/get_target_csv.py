import pickle
import pandas as pd 

def get_target_csv():

	target_dict = pickle.load(open('judge_dissent_dummy.p', 'rw'))

	target = pd.DataFrame(target_dict).T

	target.to_csv('target.csv')

if __name__ == '__main__':
	get_target_csv()
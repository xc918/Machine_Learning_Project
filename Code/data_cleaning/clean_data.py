import pandas as pd
import numpy as np
import random
import datetime
import pickle

def load_data():
	vote_level = pd.read_stata('100Votelevel_touse.dta')
	return vote_level

def fill_na(vote_level):
	drop_feature = ['dissentdate','racenotes','Circuitjudge6','Circuitjudge5','AppointmentDate5','AppointmentDate6',
	                'TerminationDate5', 'TerminationDate6','RecessAppointDate5','RecessAppointDate6','Term2','Term3',
	                'Term4','seconddateaschiefjudgebegin', 'Degree4','Degree5','degreeyear5','seconddateaschiefjudgeend']

	replace_with_mean = ['quartertoelectAM','within', 'distance', 'outside', 'unknown_circuit', 'federal_cir', 'cir1', 
	                     'cir2', 'cir3', 'cir4', 'cir5', 'cir6', 'cir7', 'cir8', 'cir9', 'cir10', 'cir11', 'cir12',
	                     'StateOfResidence']

	replace_with_median = ['total','totpos','totneg','totcon','posclint','negclint','conclint','dma', 'condole', 
	                       'negdole', 'posdole', 'totald', 'totalc','experience','judge_year_appointed', 'ayear',
	                       'ageon','pres','left','hdem']

	replace_with_pad = ['date','year','yearq','quarter','month','day','quartertoelect']

	replace_with_zero = ['Writer','geniss','geniss1','geniss2','geniss3', 'geniss4','AffirmedInPart','ReversedInPart',
	                     'Reversed','VacatedInPart','Vacated','Remanded','DissentOrConcuOnlyIncluded',
	                     'Dissenting1','Dissenting2','bottomthird_ads','topthird_ads', 'Lowestfract','SecondHighestfract',
	                     'Highestvotesfract','Lowest','SecondHighest','Highestvotes','otherfract','thirdfract',
	                     'othervotestotalpercent', 'thirdvotestotalpercent','demvotesmajorpercent','repvotesmajorpercent',
	                     'demvotestotalpercent', 'repvotestotalpercent','demvotes', 'repvotes', 'thirdvotes', 'othervotes',
	                     'totalvotes','electoralothervotes','electoraldemvotes','tightness_popularvote', 'electoralvote', 
	                     'electoralrepvotes', 'repfract', 'demfract','elevated2','minority','majorityparty','pusattorney',
	                     'retirenextyear','fourties','score','x_pago','pres_correct2','x_ageon70ormore','x_ageon40s', 
	                     'x_ageon50s','x_ageon60s', 'x_ageon40orless','idtocorrrect','TonotInclude',
	                     'judgeidentificationnumber','birthday','birthyear','birthmonth','deathday','deathmonth','deathyear',
	                     'x_crossa', 'x_pindreg1', 'x_plawprof', 'x_pscab', 'x_pcab', 'x_pusa', 'x_pssenate', 'x_paag', 
	                     'x_psp', 'x_pslc', 'x_pssc', 'x_pshouse', 'x_psg', 'x_psgo', 'x_psenate', 'x_psatty', 'x_pmayor', 
	                     'x_plocct', 'x_phouse', 'x_pgov', 'x_pda', 'x_pcc', 'x_pccoun', 'x_pausa', 'x_evangelical',
	                     'x_pag', 'x_pada', 'x_llm_sjd', 'x_noreligion', 'x_catholic', 'x_jewish', 'x_black', 'x_nonwhite', 
	                     'x_female','x_b10s', 'x_b20s', 'x_b30s', 'x_b40s', 'x_b50s', 'MajOpinionWordCount', 
	                     'MajSelfCertainWords', 'minOpinionWordCount1','MinSelfCertainWords1', 'ConcurenceWordCount1', 
	                     'ConcurSelfCertainWords1','minOpinionWordCount2', 'MinSelfCertainWords2', 'ConcurenceWordCount2',
	                     'ConcurSelfCertainWords2', 'Term','Committeeaction','ResidenceCity']

	replace_with_one = ['gender']

	replace_with_NONE = ['JudgeCONCURRING','senatevoicevote','placeofbirthstate','raceorethnicity',
	                     'partyaffiliationofpresident','nameofschool1', 'degree1', 'nameofschool2', 'degree2',
	                    'congresi','Author']

	replace_with_new = ['vicelastnamepredecessor', 'vicefirstnamepredecessor']

	replace_with_minusone = ['reversedummy','reverseandremand', 'reversenoremand', 
	                         'affirmdummy', 'Divided', 'Treat','Divided','Affirmed', 'reversenoremand','affirmdummy',
	                         'TypeOfCourt','visiting','JudgesfromThecircuit','Public1', 'Private1','Public2', 'Private2',
	                         'Public3', 'Private3','Public4', 'Private4', 'Public5', 'Private5','x_pprivate','x_pasatty', 
	                         'x_pgovt','Circuitjudge','Circuitjudge2','Circuitjudge1','Circuitjudge3','Circuitjudge4',
	                         'season','quarter2','Degree1','Degree2','Degree3','Treat','party_Updated','party','appres',
	                         'aba','hdem','hrep', 'sdem', 'srep', 'hother', 'sother','unityi']

	replace_with_rand_0_1 = ['inexperience']

	replace_with_1970 = ['BecameSenior','startdate']

	replace_with_1700 = ['AppointmentDate','AppointmentDate1','AppointmentDate2','AppointmentDate3','AppointmentDate4',
	                     'TerminationDate','TerminationDate1','TerminationDate2','TerminationDate3','TerminationDate4',
	                     'RecessAppointDate1', 'RecessAppointDate2','RecessAppointDate3','RecessAppointDate4',
	                     'SenateConfirmationdate','deathdate','dateaschiefjudgebegin','Committeeactiondate',
	                     'dateaschiefjudgeend']

	for i in drop_feature:
	    vote_level = vote_level.drop(i,1)
	    
	for i in replace_with_mean:
	    vote_level[i] = vote_level[i].fillna(vote_level[i].dropna().mean())
	    
	for i in replace_with_median:
	    vote_level[i] = vote_level[i].fillna(vote_level[i].dropna().median())

	for i in replace_with_pad:
	    vote_level[i] = vote_level[i].fillna(method = 'pad')
	    
	for i in replace_with_zero:
	    vote_level[i] = vote_level[i].fillna(0)

	for i in replace_with_one:
	    vote_level[i] = vote_level[i].fillna(1)
	    
	for i in replace_with_minusone:
	    vote_level[i] = vote_level[i].fillna(-1)

	for i in replace_with_1970:
	    vote_level[i] = vote_level[i].fillna(np.datetime64('1970-01-01'))
	for i in replace_with_1700:
	    vote_level[i] = vote_level[i].fillna(np.datetime64('1700-01-01'))

	for i in replace_with_NONE:
	    vote_level[i] = vote_level[i].fillna('NONE')

	for i in replace_with_new:
	    vote_level[i] = vote_level[i].fillna('new')

	vote_level['inexperience'] = vote_level['inexperience'].fillna(random.randint(0,1))

	# replace ',' by '_' for MapReduce process
	vote_level['vicelastnamepredecessor'] = vote_level['vicelastnamepredecessor'].map(lambda x: '_'.join(x.strip().split(',')))
	vote_level['vicefirstnamepredecessor'] = vote_level['vicefirstnamepredecessor'].map(lambda x: '_'.join(x.strip().split(',')))
	vote_level['songername'] = vote_level['songername'].map(lambda x: '_'.join(x.strip().split(',')))

	# convert 'ageon' and 'birthyear' to categorical variable
	vote_level['ageon'] = vote_level['ageon'].map(lambda x: int((x-30)/10) if x < 70 else 4)
	vote_level['birthyear'] = vote_level['birthyear'].map(lambda x: int((x-1880)/20) if x > 1900 else 0)

	return vote_level


def select_feature(vote_level):
	feature_to_be_used = ['caseid', 'date', 'Circuit', 'MajOpinionWordCount', 'MajSelfCertainWords', 
	                      'minOpinionWordCount2', 'MinSelfCertainWords2', 'ConcurenceWordCount2', 
	                      'ConcurSelfCertainWords2', 'geniss', 'Treat', 'PossibleTypoInDissenterOrJudge', 
	                      'RehearingOrPetition', 'ConcurenceMistakenForDissent', 'distance', 'quartertoelect', 'quarter', 
	                      'yearq', 'lastquarter', 'last3', 'Circuitjudge',
	                      'j', 'songername','ageon', 'Term', 'birthyear','hdem', 'hrep', 'sdem', 'srep', 'hother', 
	                      'sother', 'State', 'presidentname', 'senatevoicevote', 'Degree1', 'Degree2', 'Degree3',
	                      'Committeeaction',  'vicelastnamepredecessor', 'vicefirstnamepredecessor', 'placeofbirthstate', 
	                      'party_Updated', 'district', 'gender', 'raceorethnicity', 'partyaffiliationofpresident', 
	                      'nameofschool1', 'nameofschool2', 'District_Circuit', 'pres', 'left', 'StateOfResidence', 
	                      'ResidenceCity', 'appres', 'aba', 'congresi', 'unityi']
	return vote_level[feature_to_be_used]


def get_col_names(vote_level_selected):
	cols = vote_level_selected.columns.tolist()
	case_info = cols[0:21]
	judge_info = cols[22:]
	col_names = []

	for i in case_info:
	    col_names.append('case_' + i)
	    
	for i in judge_info:
	    col_names.append('J1_' + i)
	    
	for i in judge_info:
	    col_names.append('J2_' + i)
	    
	interact = ['inter_age','inter_term','inter_birthyear','inter_presidentname','inter_predecessor',
	            'inter_party','inter_gender','inter_raceorethnicity','inter_partyaffiliationofpresident',
	            'inter_state','inter_appres','inter_aba','inter_unity','inter_school','dissent_dummy',
	            'sit_3mo','sit_6mo','sit_1yr','sit_before','previous_dissent_rate']
	col_names.append(interact)
	with open('col_names','w') as f:
    	pickle.dump(col_names,f)


def clean_data():
	vote_level = load_data()
	vote_level = fill_na(vote_level)
	vote_level = select_feature(vote_level)
	vote_level.to_csv('votelevel_cleaned.csv', index=False)
	get_col_names(vote_level)

def merge_mapreduce():
    interact_col_names = pickle.load('col_names.p')
    pd.options.display.float_format = '{:,.6f}'.format
    merged = pd.read_csv('MapReduce/data_mapreduce.csv', names=interact_col_names)
    merged = merged.drop(['case_caseid', 'case_date', 'J1_songername', 'J2_songername', 'J1_nameofschool1',
	                      'J1_nameofschool2', 'J2_nameofschool1', 'J2_nameofschool2'], 1)
    merged.to_csv('data_mapreduce_clean.csv', index=False)


def main():
	#prepare data for MapReduce
	clean_data()
	#after MapReduce, call function below
	merge_mapreduce()

if __name__ == '__main__':
	clean_data()

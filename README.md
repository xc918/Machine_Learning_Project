# User Guide
- DS-GA-1003  Final Project
- Team Member:
  - Lanyu Shang(ls3882) ls3882@nyu.edu
  - Xing Cui(xc918) xc918@nyu.edu
  - Junchao Zheng(jz2327) jz2327@nyu.edu

- Advisor:
  - Dr. Daniel Li Chen

##### 
### Part1 : Code Guide

1. We have two datasets: '100Votelevel_touse.dta' and '100CASELEVEL_Touse.dta'. '100Votelevel_touse.dta' is used to extract case information and judge information.

2. data cleaning

 - Change the path to the original file '100Votelevel_touse.dta' in   'clean_data.py'.
 
 - In tarminal, type in 
   ```sh
   $ python clean_data.py
   ```
 - The output is 'votelevel_cleaned.csv'.

3. Target Generation

 - Change the path to 'votelevel_cleaned.csv' in 'target_generation.py'.
 
 - To generate the target which indicates the agreement between 2 judges,
   ```sh
   python target_generation.py
   ```
 - The output is 'case_pro_list.p' and 'case_dict.p'.
 
 - Hand coding part: In 'case_pro_list.p' there are cases where the judges' names are in bad format so we need to hand code this part to get the target for the case. It contains about 1000 bad entries.
 
 - After handcoing, type in 
   ```sh
   python get_target_csv.py
   ```
   Then we will get the .csv file for target 'target.csv'.
   
4. MapReduce
 - Run the MapReduce code locally or on Hadoop to generate the dataset we need, in a format of 'case_information + judge1's_information + judge2's_information + inter+information + target'.
    ```sh
    cat xxx.csv | python map_interact.py | sort -n | python reduce_interact.py > output1
    cat xxx.csv | python map_sit.py | sort -n | python reduce_sit.py > output2
    cat xxx.csv | python map_name_date.py | sort -n | python reduce_name_date.py > output3
    ```
 - Then, type in
    ```sh
    python af_mapreduce.py
    ```
    
 - The output is 'data_mapreduce_clean.csv'.

5. Model Fitting

 - Change the path to the file '0504_normalize_data.csv'
 
 - In terminal, type in 
   ```sh
   python fit_model.py
   ```
 - Output: 'output_plot_auc.csv' for AUC plotting.
 
6. F-test  

 - Change the path to the file '0504_normalize_data.csv'.
 
 - In tarminal, type in 
   ```sh
   $ python f_test.py
   ```
 - Output: two list: one contains the name for the column and the other contains the corresponding f-value for the column.

### Part2 : Poster

 - The poster is made by Latex. The template is from ShareLatex. Final version    poster is available.

### Part3 : Report

 - The final report is made by Latex. It contains all steps of the project.
The content before formatting final version is in the Google Doc link:

    https://drive.google.com/open?id=1qdkE-ooCI92W-chToukwxkZQXkzeRAR7toqbCmT7gXE


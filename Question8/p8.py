#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from tqdm import trange


# In[2]:


df = pd.read_excel("https://censusindia.gov.in/2011Census/Language-2011/DDW-C18-0000.xlsx")

age_groups = ["5-9", "10-14", "15-19", "20-24", "25-29", "30-49", "50-69", "70+", "Age not stated"]

df1 = df.loc[df["Unnamed: 4"].isin(age_groups)]
df1 = df1.loc[df["Unnamed: 3"].isin(["Total"])]

df1.rename(columns = {"C-18 POPULATION BY BILINGUALISM, TRILINGUALISM, AGE AND SEX": "state-code"}, inplace = True)


# In[3]:


final_list1 ,final_list2, final_list3 = [], [], []

for i in trange(36):

    age_df = pd.read_excel(f"https://censusindia.gov.in/2011census/C-series/c-14/DDW-{i:02}00C-14.xls")
    age_df.rename(columns = {'C-14 POPULATION IN FIVE YEAR AGE-GROUP BY RESIDENCE AND SEX ':'age-group'}, inplace = True)

    age_df1 = age_df.iloc[6:25,[4,6,7]]
    age_df1

    ## fixing the age-groupes that were not present in both the dataset
    age_30_49 = age_df1.iloc[7:11,[1,2]].sum()
    age_50_69 = age_df1.iloc[11:15,[1,2]].sum()
    age_70_up = age_df1.iloc[15:18,[1,2]].sum()

    age_df1.iloc[7] = {
        "age-group": "30-49",
        "Unnamed: 6": age_30_49[0],
        "Unnamed: 7": age_30_49[1]
    }
    age_df1.iloc[11] = {
        "age-group": "50-69",
        "Unnamed: 6": age_50_69[0],
        "Unnamed: 7": age_50_69[1]
    }
    age_df1.iloc[15] = {
        "age-group": "70+",
        "Unnamed: 6": age_70_up[0],
        "Unnamed: 7": age_70_up[1]
    }

    age_df1.drop(index = np.where(age_df1['age-group'].isin(age_groups) == False)[0]+6, inplace = True)
    age_df1.columns = ['age-group', 'total-male', 'total-female']
    ########################################################################

    state_data = df1.iloc[np.where(df1['state-code'] == f'{i:02}')][['Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 10']]

    state_data.columns = ['age-group', '2-male', '2-female', '3-male', '3-female']
    # for eaxctly 1 language
    state_data['1-male'] = age_df1['total-male'].values - state_data['2-male'].values
    state_data['1-female'] = age_df1['total-female'].values - state_data['2-female'].values
    # for exactly 2 languages
    state_data['2-male'] = state_data['2-male'].values - state_data['3-male'].values
    state_data['2-female'] = state_data['2-female'].values - state_data['3-female'].values

    ## collecting percentages for all the age groups
    state_data['percent_male_1'] = state_data['1-male'].values/age_df1['total-male'].values
    state_data['percent_female_1'] = state_data['1-female'].values/age_df1['total-female'].values
    state_data['percent_male_2'] = state_data['2-male'].values/age_df1['total-male'].values
    state_data['percent_female_2'] = state_data['2-female'].values/age_df1['total-female'].values
    state_data['percent_male_3'] = state_data['3-male'].values/age_df1['total-male'].values
    state_data['percent_female_3'] = state_data['3-female'].values/age_df1['total-female'].values
    ########################################################################

    ## for only 1 language
    # for male percentages
    temp = state_data.sort_values(by = 'percent_male_1', ascending = False)
    age_grp_male = temp['age-group'].iloc[0]
    percent_male = temp['percent_male_1'].iloc[0]
    # for female percentages
    temp = state_data.sort_values(by = 'percent_female_1', ascending = False)
    age_grp_female = temp['age-group'].iloc[0]
    percent_female = temp['percent_female_1'].iloc[0]

    final_list1.append([age_grp_male, percent_male, age_grp_female, percent_female])


    ## for exactly 2 languages
    # for male percentages
    temp = state_data.sort_values(by = 'percent_male_2', ascending = False)
    age_grp_male = temp['age-group'].iloc[0]
    percent_male = temp['percent_male_2'].iloc[0]
    # for female percentages
    temp = state_data.sort_values(by = 'percent_female_2', ascending = False)
    age_grp_female = temp['age-group'].iloc[0]
    percent_female = temp['percent_female_2'].iloc[0]

    final_list2.append([age_grp_male, percent_male, age_grp_female, percent_female])

    ## for 3 or more language
    # for male percentages
    temp = state_data.sort_values(by = 'percent_male_3', ascending = False)
    age_grp_male = temp['age-group'].iloc[0]
    percent_male = temp['percent_male_3'].iloc[0]
    # for female percentages
    temp = state_data.sort_values(by = 'percent_female_3', ascending = False)
    age_grp_female = temp['age-group'].iloc[0]
    percent_female = temp['percent_female_3'].iloc[0]

    final_list3.append([age_grp_male, percent_male, age_grp_female, percent_female])


# In[4]:


state_codes = []
for i in range(36):
    state_codes.append(f'{i:02}')

#os.chdir('..')
if not os.path.exists("outputs"):
    os.mkdir("outputs")

final_list = pd.DataFrame(final_list1)
final_list.insert(0,'state/ut', state_codes)
final_list.columns = ["state/ut", "age-group-males", "ratio-males", "age-group-females", "ratio-females"]

path = os.path.join(os.getcwd(), "outputs", "age-gender-c.csv")
final_list.to_csv(path, index = False)
print("age-gender-c created!")


final_list = pd.DataFrame(final_list2)
final_list.insert(0,'state/ut', state_codes)
final_list.columns = ["state/ut", "age-group-males", "ratio-males", "age-group-females", "ratio-females"]

path = os.path.join(os.getcwd(), "outputs", "age-gender-b.csv")
final_list.to_csv(path, index = False)
print("age-gender-b created!")

final_list = pd.DataFrame(final_list3)
final_list.insert(0,'state/ut', state_codes)
final_list.columns = ["state/ut", "age-group-males", "ratio-males", "age-group-females", "ratio-females"]

path = os.path.join(os.getcwd(), "outputs", "age-gender-a.csv")
final_list.to_csv(path, index = False)
print("age-gender-a created!")


# In[5]:


#####################################################################################################


# In[ ]:

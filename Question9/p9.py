#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from tqdm import trange


# In[2]:


df = pd.read_excel("https://censusindia.gov.in/2011Census/Language-2011/DDW-C19-0000.xlsx")

literacy = ["Illiterate", "Literate but below primary", "Primary but below middle", "Middle but below matric/secondary",
            "Matric/Secondary but below graduate", "Graduate and above"]

df1 = df.loc[df["Unnamed: 4"].isin(literacy)]
df1 = df1.loc[df["Unnamed: 3"].isin(["Total"])]

df1.rename(columns = {"C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX": "state-code"}, inplace = True)
df1.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis = 1, inplace = True)
df1.drop(['Unnamed: 5', 'Unnamed: 8'], axis = 1, inplace = True)
df1.columns = ['state-code','literacy-group','2-male','2-female','3-male','3-female']


# In[3]:


lit_df = pd.read_excel("https://censusindia.gov.in/2011census/C-series/C-08/DDW-0000C-08.xlsx")


# In[4]:


final_list1 ,final_list2, final_list3 = [], [], []


# In[5]:


for i in trange(36):
    state_lit_df = lit_df.iloc[np.where(lit_df.iloc[:,1] == f'{i:02}')].iloc[0]

    new_state_df = pd.DataFrame()
    new_state_df.insert(0,'literacy-group',literacy)

    new_state_df['total-male'] = [state_lit_df[10], state_lit_df[16] + state_lit_df[19], state_lit_df[22],
                                 state_lit_df[25], state_lit_df[28] + state_lit_df[31] + state_lit_df[34] + state_lit_df[37],
                                 state_lit_df[40]]
    new_state_df['total-female'] = [state_lit_df[11], state_lit_df[17] + state_lit_df[20], state_lit_df[23],
                                 state_lit_df[26], state_lit_df[29] + state_lit_df[32] + state_lit_df[35] + state_lit_df[38],
                                 state_lit_df[41]]

    ## calculating number of males and females who speak only one languages
    temp_state_df = df1.where((df1['state-code']) == f'{i:02}').dropna()
    temp_state_df['1-male'] = new_state_df['total-male'].values - temp_state_df['2-male'].values
    temp_state_df['1-female'] = new_state_df['total-female'].values - temp_state_df['2-female'].values
    ## calculating number of males and females who speak exactly two languages
    temp_state_df['2-male'] = temp_state_df['2-male'].values - temp_state_df['3-male'].values
    temp_state_df['2-female'] = temp_state_df['2-female'].values - temp_state_df['3-female'].values

    ## collecting percentages for all the literacy groups
    temp_state_df['percent_male_1'] = temp_state_df['1-male'].values / new_state_df['total-male'].values
    temp_state_df['percent_female_1'] = temp_state_df['1-female'].values / new_state_df['total-female'].values
    temp_state_df['percent_male_2'] = temp_state_df['2-male'].values / new_state_df['total-male'].values
    temp_state_df['percent_female_2'] = temp_state_df['2-female'].values / new_state_df['total-female'].values
    temp_state_df['percent_male_3'] = temp_state_df['3-male'].values / new_state_df['total-male'].values
    temp_state_df['percent_female_3'] = temp_state_df['3-female'].values / new_state_df['total-female'].values

    ## for only 1 language
    # for male percentages
    temp = temp_state_df.sort_values(by = 'percent_male_1', ascending = False)
    lit_grp_male = temp['literacy-group'].iloc[0]
    percent_male = temp['percent_male_1'].iloc[0]
    # for female percentages
    temp = temp_state_df.sort_values(by = 'percent_female_1', ascending = False)
    lit_grp_female = temp['literacy-group'].iloc[0]
    percent_female = temp['percent_female_1'].iloc[0]

    final_list1.append([lit_grp_male, percent_male, lit_grp_female, percent_female])

    ## for exactly 2 language
    # for male percentages
    temp = temp_state_df.sort_values(by = 'percent_male_2', ascending = False)
    lit_grp_male = temp['literacy-group'].iloc[0]
    percent_male = temp['percent_male_2'].iloc[0]
    # for female percentages
    temp = temp_state_df.sort_values(by = 'percent_female_2', ascending = False)
    lit_grp_female = temp['literacy-group'].iloc[0]
    percent_female = temp['percent_female_2'].iloc[0]

    final_list2.append([lit_grp_male, percent_male, lit_grp_female, percent_female])

    ## for 3 or more language
    # for male percentages
    temp = temp_state_df.sort_values(by = 'percent_male_3', ascending = False)
    lit_grp_male = temp['literacy-group'].iloc[0]
    percent_male = temp['percent_male_3'].iloc[0]
    # for female percentages
    temp = temp_state_df.sort_values(by = 'percent_female_3', ascending = False)
    lit_grp_female = temp['literacy-group'].iloc[0]
    percent_female = temp['percent_female_3'].iloc[0]

    final_list3.append([lit_grp_male, percent_male, lit_grp_female, percent_female])


# In[6]:


state_codes = []
for i in range(36):
    state_codes.append(f'{i:02}')

#os.chdir('..')
if not os.path.exists("outputs"):
    os.mkdir("outputs")

final_list = pd.DataFrame(final_list1)
final_list.insert(0,'state/ut', state_codes)
final_list.columns = ["state/ut", "literacy-group-males", "ratio-males", "literacy-group-females", "ratio-females"]

path = os.path.join(os.getcwd(), "outputs", "literacy-gender-c.csv")
final_list.to_csv(path, index = False)
print("literacy-gender-c created!")

final_list = pd.DataFrame(final_list2)
final_list.insert(0,'state/ut', state_codes)
final_list.columns = ["state/ut", "literacy-group-males", "ratio-males", "literacy-group-females", "ratio-females"]

path = os.path.join(os.getcwd(), "outputs", "literacy-gender-b.csv")
final_list.to_csv(path, index = False)
print("literacy-gender-b created!")

final_list = pd.DataFrame(final_list3)
final_list.insert(0,'state/ut', state_codes)
final_list.columns = ["state/ut", "literacy-group-males", "ratio-males", "literacy-group-females", "ratio-females"]

path = os.path.join(os.getcwd(), "outputs", "literacy-gender-a.csv")
final_list.to_csv(path, index = False)
print("literacy-gender-a created!")

# In[ ]:

#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import os
from tqdm import trange

df = pd.read_excel("https://censusindia.gov.in/2011Census/Language-2011/DDW-C18-0000.xlsx")

age_groups = ["Total", "5-9", "10-14", "15-19", "20-24", "25-29", "30-49", "50-69", "70+", "Age not stated"]

df1 = df.loc[df["Unnamed: 4"].isin(age_groups)]
df1 = df1.loc[df["Unnamed: 3"].isin(["Total"])]

df1.rename(columns = {"C-18 POPULATION BY BILINGUALISM, TRILINGUALISM, AGE AND SEX": "state-code"}, inplace = True)


# In[9]:


######################################################################################################


# In[13]:


final_list = []

for i in trange(36):
    age_df = pd.read_excel(f"https://censusindia.gov.in/2011census/C-series/c-14/DDW-{i:02}00C-14.xls")
    age_df.rename(columns = {'C-14 POPULATION IN FIVE YEAR AGE-GROUP BY RESIDENCE AND SEX ':'age-group'}, inplace = True)

    age_df1 = age_df.iloc[6:25,[4,5]]
    age_df1

    ## fixing the age-groupes that were not present in both the dataset
    age_30_49 = age_df1.iloc[7:11,1].sum()
    age_50_69 = age_df1.iloc[11:15,1].sum()
    age_70_up = age_df1.iloc[15:18,1].sum()

    age_df1.iloc[7] = {
        "age-group": "30-49",
        "Unnamed: 5": age_30_49
    }
    age_df1.iloc[11] = {
        "age-group": "50-69",
        "Unnamed: 5": age_50_69
    }
    age_df1.iloc[15] = {
        "age-group": "70+",
        "Unnamed: 5": age_70_up
    }

    age_df1.drop(index = np.where(age_df1['age-group'].isin(age_groups[1:]) == False)[0]+6, inplace = True)

    total = age_df1["Unnamed: 5"]


    try:
        a = 10*i
        b = 10*(i+1)
        state_df = df1.iloc[a+1:b].copy()
        total.index = state_df.index
        state_df.loc[:,"percentage"] = state_df.loc[:,"Unnamed: 8"]/total
    except:
        state_df = df1.iloc[a+1:].copy()
        total.index = state_df.index
        state_df.loc[:,"percentage"] = state_df.loc[:,"Unnamed: 8"]/total

    state_df.sort_values(by="percentage", ascending=False, inplace = True)
    state = f'{i:02}'
    age_group = state_df["Unnamed: 4"].iloc[0]
    percentage = state_df["percentage"].iloc[0]*100
    final_list.append([state, age_group, percentage])



# In[15]:


final_list = pd.DataFrame(final_list)
final_list.columns = ["state/ut", "age-group", "percentage"]

#os.chdir('..')
if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "age-india.csv")
final_list.to_csv(path, index = False)
print("age-india.csv created!")

# In[12]:


#########################################################################################################


# In[ ]:

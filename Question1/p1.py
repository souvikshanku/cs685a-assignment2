#!/usr/bin/env python
# coding: utf-8

# In[151]:


import pandas as pd
import numpy as np
import os
from tqdm import trange


# In[5]:


urls = []
for i in range(36):
    urls.append(f"https://censusindia.gov.in/2011census/C-17/DDW-C17-{i:02}00.XLSX")

## a list containing all the state values
final_ls = []


# In[20]:


for i in trange(36):
    df = pd.read_excel(urls[i])
    
    ## filling the nan values for the 3 "Persons" columns  
    df.iloc[:,[4,9,14]] = df.iloc[:,[4,9,14]].fillna(0)
    
    lang_index = (np.where(df.iloc[:,2].notna() == True)[0])[3:]
    temp_matrix = []
    
    for j in range(len(lang_index)):
        try:
            a = lang_index[j]
            b = lang_index[j+1]
            ls = [np.array(df.iloc[:,[4,9,14]].iloc[a:b].sum())]
            ls[0][0] = ls[0][0] - ls[0][1]
            ls[0][1] = ls[0][1] - ls[0][2]
        except:
            a = lang_index[j]
            ls = [np.array(df.iloc[:,[4,9,14]].iloc[a:].sum())]        
            ls[0][0] = ls[0][0] - ls[0][1]
            ls[0][1] = ls[0][1] - ls[0][2]
        temp_matrix.append(ls)
    
    # for each state
    state_total = np.array(temp_matrix).squeeze(axis = 1).sum(axis = 0)
    # for calculating percentage
    pop_total = sum(state_total)
    state_total = [(total/pop_total) * 100 for total in state_total]
    final_ls.append(state_total)
    


# In[47]:


final_df = pd.DataFrame(final_ls)

state_codes = []
for i in range(36):
    state_codes.append(f'{i:02}')
    
final_df.index = state_codes

final_df.columns = ["percent-one", "percent-two", "percent-three"]
final_df.index.names = ["state-code"]


# In[64]:

#os.chdir('..')
if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "percent-india.csv")
if not os.path.exists("percent-india.csv"):
    final_df.to_csv(path)

print('percent-india.csv created!')

# In[ ]:





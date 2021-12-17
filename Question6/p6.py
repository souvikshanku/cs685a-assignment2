#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from tqdm import trange


# In[2]:


df = pd.read_excel("https://censusindia.gov.in/2011Census/Language-2011/DDW-C19-0000.xlsx")


# In[3]:


literacy = ["Total", "Illiterate", "Literate but below primary", "Primary but below middle", "Middle but below matric/secondary",
            "Matric/Secondary but below graduate", "Graduate and above"]

df1 = df.loc[df["Unnamed: 4"].isin(literacy)]
df1 = df1.loc[df["Unnamed: 3"].isin(["Total"])]

df1.rename(columns = {"C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX": "state-code"}, inplace = True)

lit_df = pd.read_excel("https://censusindia.gov.in/2011census/C-series/C-08/DDW-0000C-08.xlsx")


# In[4]:


final_list = []
for i in trange(36):

    state_lit_df = lit_df.iloc[np.where(lit_df.iloc[:,1] == f'{i:02}')].iloc[0]
    new_state_df = pd.DataFrame()
    new_state_df['Illiterate'] = [state_lit_df[9]]
    new_state_df['Literate but below primary'] = [state_lit_df[15] + state_lit_df[18]]
    new_state_df['Primary but below middle'] = [state_lit_df[21]]
    new_state_df['Middle but below matric/secondary'] = [state_lit_df[24]]
    new_state_df['Matric/Secondary but below graduate'] = [state_lit_df[27] + state_lit_df[30] + state_lit_df[33] + state_lit_df[36]]
    new_state_df['Graduate and above'] = [state_lit_df[39]]

    try:
        a = 7*i
        b = 7*(i+1)
        total = new_state_df
        state_df = df1[a+1:b].copy()
        percentage = state_df.iloc[:,8].reset_index().iloc[:,1]/total.T.reset_index().iloc[:,1]
        state_df.loc[:,"percentage"] = percentage.values
    except:
        a = 7*i
        total = new_state_df
        state_df = df1[a:].copy()
        state_df.loc[:,"percentage"] = state_df.loc[:,"Unnamed: 8"]/total

    state_df.sort_values(by="percentage", ascending=False, inplace = True)
    state = f'{i:02}'
    literacy = state_df["Unnamed: 4"].iloc[0]
    percentage = state_df["percentage"].iloc[0]*100
    final_list.append([state, literacy, percentage])



# In[5]:


final_list = pd.DataFrame(final_list)
final_list.columns = ["state/ut", "literacy-group", "percentage"]

#os.chdir('..')
if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "literacy-india.csv")
final_list.to_csv(path, index = False)
print("literacy-india.csv created!")


# In[ ]:


#########################################################################################################


# In[ ]:

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import copy
import os
from tqdm import trange


# In[2]:


region_dict = {
    "North": ["JAMMU & KASHMIR", "PUNJAB", "HIMACHAL PRADESH", "HARYANA", "UTTARAKHAND", "NCT OF DELHI", "CHANDIGARH"],
    "West": ["RAJASTHAN", "GUJARAT", "MAHARASHTRA", "GOA", "DADRA & NAGAR HAVELI", "DAMAN & DIU"],
    "Central": ["MADHYA PRADESH", "UTTAR PRADESH", "CHHATTISGARH"],
    "East": ["BIHAR", "WEST BENGAL", "ODISHA", "JHARKHAND"],
    "South": ["KARNATAKA", "ANDHRA PRADESH", "TAMIL NADU", "KERALA", "LAKSHADWEEP", "PUDUCHERRY"],
    "North-East": ["ASSAM", "SIKKIM", "MIZORAM", "TRIPURA", "ARUNACHAL PRADESH", "MANIPUR", "NAGALAND", "MIZORAM", "ANDAMAN & NICOBAR ISLANDS"]
}

lang_dict = {
    "North": {},
    "West": {},
    "Central": {},
    "East": {},
    "South": {},
    "North-East": {}
}

lang_dict_mothertongue = copy.deepcopy(lang_dict)


# In[3]:


for i in trange(1,36):
    df = pd.read_excel(f"https://censusindia.gov.in/2011census/C-17/DDW-C17-{i:02}00.XLSX")
    lang_index = (np.where(df.iloc[:,2].notna() == True)[0])[3:]    ## language indices
    state = df.iloc[lang_index[0],1]

    ## for finding the region the state belongs to
    for key in region_dict.keys():
        if state in region_dict[key]:
            break
    region = key

    ## lang_dict will contain number of people speaking different languages region-wise
    for index in lang_index:
        language = df.iloc[index,3]
        first_lang_pop = df.iloc[index,4]                      ## number of people whose first language (i.e mother tongue) is "language"
        indx2 = df["Unnamed: 8"] == language
        second_lang_pop = df.loc[indx2, "Unnamed: 9"].sum()    ## number of people whose second language is "language"
        indx3 = df["Unnamed: 13"] == language
        third_lang_pop = df.loc[indx3, "Unnamed: 14"].sum()    ## number of people whose third language is "language"
        pop = first_lang_pop + second_lang_pop + third_lang_pop

        ## considering all level of language speakers
        if language in lang_dict[region].keys():
            lang_dict[region][language] += pop
        else:
            lang_dict[region][language] = pop

        ## for mothertongues
        if language in lang_dict_mothertongue[region].keys():
            lang_dict_mothertongue[region][language] += first_lang_pop
        else:
            lang_dict_mothertongue[region][language] = first_lang_pop




# In[4]:


## for mothertongues
for region in lang_dict_mothertongue:
    lang_dict_mothertongue[region] = sorted(lang_dict_mothertongue[region], key=lambda x : lang_dict_mothertongue[region][x], reverse = True)

final_list = []

for region in lang_dict_mothertongue:
    top_three_languages = lang_dict_mothertongue[region][:3]
    final_list.append(top_three_languages)

final_df1 = pd.DataFrame(final_list, columns = ["language-1", "language-2", "language-3"], index = region_dict.keys())
final_df1.index.names = ['region']


# In[5]:


## For all level of language speakers
for region in lang_dict:
    lang_dict[region] = sorted(lang_dict[region], key=lambda x : lang_dict[region][x], reverse = True)

final_list = []

for region in lang_dict:
    top_three_languages = lang_dict[region][:3]
    final_list.append(top_three_languages)

final_df2 = pd.DataFrame(final_list, columns = ["language-1", "language-2", "language-3"], index = region_dict.keys())
final_df2.index.names = ['region']

final_df1.sort_values(by = 'region', inplace = True)
final_df2.sort_values(by = 'region', inplace = True)

# In[6]:


# final_dfs
#os.chdir('..')
if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "region-india-a.csv")
final_df1.to_csv(path)
print("region-india-a.csv created!")
path = os.path.join(os.getcwd(), "outputs", "region-india-b.csv")
final_df2.to_csv(path)
print("region-india-b.csv created!")


# In[7]:


#################################################################################################

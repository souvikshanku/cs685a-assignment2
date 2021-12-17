#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import scipy.stats.distributions as dist
import os
from tqdm import trange

rural_urban_df = pd.read_excel(r'http://censusindia.gov.in/pca/DDW_PCA0000_2011_Indiastatedist.xlsx')

language_df = pd.read_excel(r'https://censusindia.gov.in/2011Census/Language-2011/DDW-C18-0000.xlsx')
language_df.rename(columns = {'C-18 POPULATION BY BILINGUALISM, TRILINGUALISM, AGE AND SEX':'state-code'}, inplace = True)
language_df = language_df.iloc[5:,:]

percentage_and_p_value1,percentage_and_p_value2,percentage_and_p_value3 = [],[],[]

for i in trange(36):
    _,total_rural,total_urban = rural_urban_df.where(rural_urban_df['State'] == i).dropna().iloc[:3,10]
    
    temp_df = language_df.where(language_df['state-code'] == f'{i:02}').dropna()
    rural_pop_1 = total_rural - temp_df.iloc[10,5]
    urban_pop_1 = total_urban - temp_df.iloc[20,5]
    rural_pop_2 = temp_df.iloc[10,5] - temp_df.iloc[10,8]
    urban_pop_2 = temp_df.iloc[20,5] - temp_df.iloc[20,8]
    rural_pop_3 = temp_df.iloc[10,8]
    urban_pop_3 = temp_df.iloc[20,8]
    
    ## for exactly 1 languages
    rural_percentage, urban_percentage = [rural_pop_1/total_rural*100, urban_pop_1/total_urban*100]
    ## calculating p-value
    p1 = rural_pop_1/total_rural
    p2 = urban_pop_1/total_urban
    p = (rural_pop_1+urban_pop_1)/(total_rural+total_urban)
    n1 = total_rural
    n2 = total_urban
    z = (p1-p2)/(np.sqrt(p*(1-p)*(1/n1 + 1/n2)))
    p_value = 2*min(dist.norm.cdf(-np.abs(z)), dist.norm.cdf(np.abs(z)))
    percentage_and_p_value1.append([urban_percentage, rural_percentage, p_value])
    
    ## for exactly 2 languages
    rural_percentage, urban_percentage = [rural_pop_2/total_rural*100, urban_pop_2/total_urban*100]
    ## calculating p-value
    p1 = rural_pop_2/total_rural
    p2 = urban_pop_2/total_urban
    p = (rural_pop_2+urban_pop_2)/(total_rural+total_urban)
    n1 = total_rural
    n2 = total_urban
    z = (p1-p2)/(np.sqrt(p*(1-p)*(1/n1 + 1/n2)))
    p_value = 2*min(dist.norm.cdf(-np.abs(z)), dist.norm.cdf(np.abs(z)))
    
    percentage_and_p_value2.append([urban_percentage, rural_percentage,p_value])
    
    
    ## for 3 or more languages
    rural_percentage, urban_percentage = [rural_pop_3/total_rural*100, urban_pop_3/total_urban*100]
    ## calculating p-value
    p1 = rural_pop_3/total_rural
    p2 = urban_pop_3/total_urban
    p = (rural_pop_3+urban_pop_3)/(total_rural+total_urban)
    n1 = total_rural
    n2 = total_urban
    z = (p1-p2)/(np.sqrt(p*(1-p)*(1/n1 + 1/n2)))
    p_value = 2*min(dist.norm.cdf(-np.abs(z)), dist.norm.cdf(np.abs(z)))
    percentage_and_p_value3.append([urban_percentage, rural_percentage,p_value])

final_df1 = pd.DataFrame(percentage_and_p_value1)
final_df2 = pd.DataFrame(percentage_and_p_value2)
final_df3 = pd.DataFrame(percentage_and_p_value3)

state_codes = []
for i in range(36):
    state_codes.append(f'{i:02}')

final_df1.index = state_codes
final_df1.columns = ["urban-percentage", "rural-percentage",  "p-value"]
final_df1.index.names = ["state-code"]

if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "geography-india-a.csv")
final_df1.to_csv(path)
print("geography-india-a.csv created!")
#########

final_df2.index = state_codes

final_df2.columns = ["urban-percentage", "rural-percentage",  "p-value"]
final_df2.index.names = ["state-code"]

if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "geography-india-b.csv")
final_df2.to_csv(path)
print("geography-india-b.csv created!")
##########
final_df3.index = state_codes

final_df3.columns = ["urban-percentage", "rural-percentage",  "p-value"]
final_df3.index.names = ["state-code"]

if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "geography-india-c.csv")
final_df3.to_csv(path)
print("geography-india-c.csv created!")

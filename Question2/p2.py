#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import scipy.stats.distributions as dist
import os
from tqdm import trange

######################################################################################################

urls = []
for i in range(36):
    urls.append(f"https://censusindia.gov.in/2011census/C-17/DDW-C17-{i:02}00.XLSX")

percentage_and_p_value1,percentage_and_p_value2,percentage_and_p_value3 = [],[],[]

for i in trange(36):
    df = pd.read_excel(urls[i])
    
    lang_pop = df.iloc[:,[5,6,10,11,15,16]].fillna(0).iloc[5:].sum(axis = 0)
    total_state_pop = df.iloc[:,[5,6]].fillna(0).iloc[5:].sum(axis = 0)

    exactly_one_male = lang_pop[0] - lang_pop[2]
    two_male = lang_pop[2] - lang_pop[4]
    three_male = lang_pop[4]

    exactly_one_female = lang_pop[1] - lang_pop[3]
    two_female = lang_pop[3] - lang_pop[5]
    three_female = lang_pop[5]


    ## for exactly 1 languages
    male_percentage, female_percentage = exactly_one_male/total_state_pop[0]*100, exactly_one_female/total_state_pop[1]*100
    ## calculating p-value
    p1 = exactly_one_male/total_state_pop[0]
    p2 = exactly_one_female/total_state_pop[1]
    p = (exactly_one_male+exactly_one_female)/sum(total_state_pop)
    n1 = total_state_pop[0]
    n2 = total_state_pop[1]
    z = (p1-p2)/(np.sqrt(p*(1-p)*(1/n1 + 1/n2)))
    p_value = 2*min(dist.norm.cdf(-np.abs(z)), dist.norm.cdf(np.abs(z)))
    percentage_and_p_value1.append([male_percentage,female_percentage,p_value])

    ## for exactly 2 languages
    male_percentage, female_percentage = two_male/total_state_pop[0]*100, two_female/total_state_pop[1]*100
    ## calculating p-value
    p1 = two_male/total_state_pop[0]
    p2 = two_female/total_state_pop[1]
    p = (two_male+two_female)/sum(total_state_pop)
    n1 = total_state_pop[0]
    n2 = total_state_pop[1]
    z = (p1-p2)/(np.sqrt(p*(1-p)*(1/n1 + 1/n2)))
    p_value = 2*min(dist.norm.cdf(-np.abs(z)), dist.norm.cdf(np.abs(z)))
    percentage_and_p_value2.append([male_percentage,female_percentage,p_value])


    ## for 3 or more languages
    male_percentage, female_percentage = three_male/total_state_pop[0]*100, three_female/total_state_pop[1]*100
    ## calculating p-value
    p1 = three_male/total_state_pop[0]
    p2 = three_female/total_state_pop[1]
    p = (three_male+three_female)/sum(total_state_pop)
    n1 = total_state_pop[0]
    n2 = total_state_pop[1]
    z = (p1-p2)/(np.sqrt(p*(1-p)*(1/n1 + 1/n2)))
    p_value = 2*min(dist.norm.cdf(-np.abs(z)), dist.norm.cdf(np.abs(z)))
    percentage_and_p_value3.append([male_percentage,female_percentage,p_value])

final_df1 = pd.DataFrame(percentage_and_p_value1)
final_df2 = pd.DataFrame(percentage_and_p_value2)
final_df3 = pd.DataFrame(percentage_and_p_value3)

state_codes = []
for i in range(36):
    state_codes.append(f'{i:02}')
    
final_df1.index = state_codes
final_df2.index = state_codes
final_df3.index = state_codes

final_df1.columns = ["male-percentage", "female-percentage",  "p-value"]
final_df1.index.names = ["state-code"]

final_df2.columns = ["male-percentage", "female-percentage",  "p-value"]
final_df2.index.names = ["state-code"]

final_df3.columns = ["male-percentage", "female-percentage",  "p-value"]
final_df3.index.names = ["state-code"]

if not os.path.exists("outputs"):
    os.mkdir("outputs")

path = os.path.join(os.getcwd(), "outputs", "gender-india-a.csv")
final_df1.to_csv(path)
print("gender-india-a.csv created!")

path = os.path.join(os.getcwd(), "outputs", "gender-india-b.csv")
final_df2.to_csv(path)
print("gender-india-b.csv created!")

path = os.path.join(os.getcwd(), "outputs", "gender-india-c.csv")
final_df3.to_csv(path)
print("gender-india-c.csv created!")

#######################################################################################################


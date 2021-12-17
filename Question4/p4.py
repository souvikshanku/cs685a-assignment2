#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
#from tqdm import trange


# In[2]:

try:
    path = os.path.join(os.getcwd(), "outputs", "percent-india.csv")
    #print(path)
    df = pd.read_csv(path)


    # In[3]:


    df["3-to-2-ratio"] = df["percent-three"]/df["percent-two"]
    df["2-to-1-ratio"] = df["percent-two"]/df["percent-one"]


    # In[34]:


    ## For 3-to-2 ratios
    df_3_to_2 = df.sort_values(by = "3-to-2-ratio", ascending=False)
    best = list(df_3_to_2.index[:3])
    best_state = [df_3_to_2.loc[i]['3-to-2-ratio'] for i in best]
    worst = list(df_3_to_2.index[:-4:-1])
    worst_state = [df_3_to_2.loc[i]['3-to-2-ratio'] for i in worst]
    #worst.reverse()

    best_worst = []
    for i in range(len(best)):
        best_worst.append([best[i],best_state[i]])
    for j in range(len(worst)):
        best_worst.append([worst[j],worst_state[j]])

    best_worst_df1 = pd.DataFrame(best_worst)
    best_worst_df1.columns = ["state-code","3-to-2-ratio"]


    # In[35]:


    ## For 2-to-1 ratios
    df_2_to_1 = df.sort_values(by = "2-to-1-ratio", ascending=False)
    best = list(df_2_to_1.index[:3])
    best_state = [df_2_to_1.loc[i]['2-to-1-ratio'] for i in best]
    worst = list(df_2_to_1.index[:-4:-1])
    worst_state = [df_2_to_1.loc[i]['2-to-1-ratio'] for i in worst]
    #worst.reverse()

    best_worst = []
    for i in range(len(best)):
        best_worst.append([best[i],best_state[i]])
    for j in range(len(worst)):
        best_worst.append([worst[j],worst_state[j]])

    best_worst_df2 = pd.DataFrame(best_worst)
    best_worst_df2.columns = ["state-code","2-to-1-ratio"]


    # In[37]:

    #os.chdir('..')
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    path = os.path.join(os.getcwd(), "outputs", "3-to-2-ratio.csv")
    best_worst_df1.to_csv(path, index = False)
    print("3-to-2-ratio.csv created!")

    path = os.path.join(os.getcwd(), "outputs", "2-to-1-ratio.csv")
    best_worst_df2.to_csv(path, index = False)
    print("2-to-1-ratio.csv created!")

except:
    print("percent-india.csv not found! Please run percent-india.sh in Question1 folder first.")


# In[ ]:

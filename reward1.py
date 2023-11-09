#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import numpy as np


# In[2]:


columns = ['day', 'hospitalizeNum', 'isolateNum', 'quarantineNum', 'confineNum',
       'free', 'CurrentHealthy', 'CurrentInfected', 'CurrentEffective','CurrentSusceptible', 'CurrentIncubation', 'CurrentDiscovered', 'CurrentCritical', 'CurrentRecovered',
       'AccDiscovered', 'AccCritical', 'AccAcquaintance', 'AccStranger', 'measurement'] 

# Here are some consts for metrics
I_threshold = 1000
Q_threshold = 100000
Q_weight = 1
time = 59 # The last day of our simulation


# In[3]:


def process_file(file):
    # Read data

    df = pd.read_csv(file, sep=',', engine='python', header=None)
    df.columns = columns

    # Accumulate 
    for item in ['hospitalizeNum', 'isolateNum', 'quarantineNum', 'confineNum']:
        sum = 0
        list_sum = []
        ind = 0
        l = len(df[item])
        while ind < l:
            sum += df[item][ind]
            list_sum.append(sum)
            if df["day"][ind] == time:
                sum = 0
            ind += 1
        df["sum_"+item] = np.array(list_sum)
    return df


# In[4]:


def get_I_Q(df, time):
    # Get I and Q value at the given time

    df_sub = df[df["day"]==time]
    I = df_sub["CurrentInfected"].mean()

    inHospital_mean = df_sub["sum_hospitalizeNum"].mean()
    isolateNum_mean = df_sub["sum_isolateNum"].mean()
    confineNum_mean = df_sub["sum_confineNum"].mean()
    quarantineNum_mean = df_sub["sum_quarantineNum"].mean()
    Q = 1 *  inHospital_mean + 0.5 * isolateNum_mean+ 0.3 * quarantineNum_mean + 0.2 * confineNum_mean

    return I, Q


# In[5]:


def get_least_Q_score(I, Q, I_threshold):
    score = np.copy(Q)
    score[I > I_threshold] = 1e6

    return score


# In[6]:


def get_exp_score(I, Q, I_threshold, Q_threshold, Q_weight):
    I_score = np.exp(I/I_threshold)
    Q_score = Q_weight * (np.exp(Q/ Q_threshold))
    
    return I_score + Q_score

#
# # In[7]:
# if __name__ == "__main__":
#     import os
#     import sys
#     print(sys.path[0])
#     df = process_file("/Users/d/work/xin/starter-kit/examples/results/cnt_test.txt")
#     I, Q = get_I_Q(df, time)
#     least_Q_score = get_least_Q_score(I, Q, I_threshold)
#     exp_score = get_exp_score(I, Q, I_threshold, Q_threshold, Q_weight)
#     print(least_Q_score, exp_score)

import math
import csv
class Env:
    theat_I = 1000
    theat_Q = 100000
    Q_eff = 1
    r_hos = 1
    r_iso = 0.5
    r_qu = 0.3
    r_con = 0.2

    def __init__(self):
        self.Q = 0
        self.state_value = 0

    def get_state_value(self,day):
        I = 0
        with open('./examples/results/cnt_train.txt','r') as f:
            reader = csv.reader(f)
            results = list(reader)
            res = results[-1]
            print(day)
            print(int(res[0]))
            assert(int(res[0])==day-1)
            I = int(res[7])-int(res[13])
            self.Q += int(res[1])*self.r_hos
            self.Q += int(res[2])*self.r_iso
            self.Q += int(res[3])*self.r_qu
            self.Q += int(res[4])*self.r_con
        return math.exp(I/self.theat_I)+self.Q_eff*math.exp(self.Q/self.theat_Q)

    def get_reward(self,day):
        temp_value = self.get_state_value(day)
        reward = self.state_value-temp_value
        self.state_value = temp_value
        return reward
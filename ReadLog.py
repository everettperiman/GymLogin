# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 08:54:35 2020

@author: evere
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

def readLog(name="log.txt"):
    df = pd.read_csv(name,header=None)
    df.columns = ['TimeStamp', 'SlotDate', 'SlotTime', 'Spots']
    
    df['TimeStamp'] = df['TimeStamp'].apply(lambda x:
                                            dt.datetime.strptime(x, '%a %b  %w %H:%M:%S %Y'))

    xtick_list = generateTicks(df['TimeStamp'].iloc[0], df['TimeStamp'].iloc[-1])   
    
    df_unique = df['SlotTime'].unique()
    df_split = []

    for i in df_unique:
        local = []
        for data in df.itertuples():
            if data[3] == i:
                local.append(data)
        df_local = pd.DataFrame(local)
        df_local.columns = ['Index','TimeStamp', 'SlotDate', 'SlotTime', 'Spots']
        df_split.append(df_local)
    plotSeriesData(df_split)


def plotSeriesData(dfList):
    f = plt.figure()
    plt.title('Legend Outside', color='black')
    for index, data in reversed(list(enumerate(dfList))):
        timeSlot = data['SlotTime'].iloc[0][0:5]
        if index == len(dfList) - 1:
            data.plot.line(x ='TimeStamp', y = 'Spots', title = name, rot = 45, label = timeSlot, ax = f.gca())
           # ax = data.plot.line(x ='TimeStamp', y = 'Spots', title = name, rot = 45, label = timeSlot) #

        else:
            data.plot.line(x='TimeStamp', y = 'Spots', ax = f.gca(), rot = 45, label = timeSlot)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()
    
"""
def convertTime(x):
    timestamp = dt.datetime.strptime(x, '%a %b  %w %H:%M:%S %Y')
    
    return dt.datetime.strptime(TimeStamp, '%a %b  %w %H:%M:%S %Y')
"""

if __name__ == "__main__":
   # name = "gym_log.txt"
   # readLog(name)
    name = "gym_log.txt"
    readLog(name)    
    
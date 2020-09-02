# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 08:54:35 2020

@author: evere
"""

import pandas as pd
import datetime as dt

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
    
    for index, data in reversed(list(enumerate(df_split))):

        if index == len(df_split) - 1:
            print(type(data['TimeStamp'].iloc[0]))
            ax = data.plot.line(x ='TimeStamp', y = 'Spots', title = name, rot = 45, xticks = xtick_list) #
        else:
            data.plot.line(x='TimeStamp', y = 'Spots', ax=ax, rot = 45)
        
def generateTicks(time_low,time_high):

    tickList = []
    tick_count = 5
    ticks = 0
    delta = (time_high - time_low) / tick_count
    
    i = time_low
    while ticks < tick_count:
        i += delta
        tickList.append(i)
        ticks += 1

    print(type(tickList[0]))
    return tickList

if __name__ == "__main__":
   # name = "gym_log.txt"
   # readLog(name)
    name = "gym_log.txt"
    readLog(name)    
    
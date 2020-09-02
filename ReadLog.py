# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 08:54:35 2020

@author: evere
"""

import pandas as pd

def readLog(name="log.txt"):
    df = pd.read_csv(name,header=None)
    df_unique = df[4].unique()
    df_split = [[] for i in range(len(df_unique))]
    
        

    
    
if __name__ == "__main__":
    name = "pool_log.txt"
    readLog(name)
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 11:37:04 2020

@author: evere
"""
from reserve import *
import datetime
import random
import matplotlib.pyplot as plt


if __name__ == "__main__":   
    LogBot = logBot("pool.txt")
    while(True):
        LogBot.getReadings()
        LogBot.displayPlot(30)
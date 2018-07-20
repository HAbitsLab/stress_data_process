# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 13:35:07 2018

@author: zdking
"""
import pandas as pd
import os

dataPath = 'E:/Tech_Pilot1/RedCap/'
for subdir, dirs, files in os.walk(dataPath):
    for file in dirs:
        filepath = dataPath+file
        EMA = pd.read_csv(filepath)
        print 1
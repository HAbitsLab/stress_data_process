# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:10:55 2018

@author: zdking
"""
import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def convertBinary(val,mean): 
    print [val,mean]
    if val >= mean and mean > 0.0:
        x = 1
    else:
        x = 0
    return x

def ProcessEMA(EMAdf):
    prev = 0
    prevpss = 0
    returnDF = pd.DataFrame(columns = ['participant','start', 'end', 'label'])
    for index, row in EMAdf.iterrows():
        likert = row['LikertStress']
        end = row['TimeStamp']
        part = row['Participant']
        st = datetime.strptime(end, "%m/%d/%Y %H:%M") + timedelta(hours=5)
        end =  (st - datetime(1970,1,1)).total_seconds() * 1000
        start = end - 3600000
        if prev > start:
            val = float(likert + prevpss)/2
        else:
            val = likert
        retArr = [part, start, end, convertBinary(val,np.array(EMAdf.loc[EMAdf['Participant'] == part]['LikertStress']).mean())]
        returnDF.loc[-1] = retArr # adding a row
        returnDF.index = returnDF.index + 1  # shifting index
        returnDF = returnDF.sort_index()
        
    return returnDF    
    

dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/Tech_Pilot1/ECG_Accel/'
labelPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/Tech_Pilot1/RedCap/labels_EMA.csv'
labels = pd.read_csv(labelPath)
labels = ProcessEMA(labels)
Participants = ['101','102','103','104','105','106','107','108']
for part in Participants:   
    rootdir = dataPath+str(part)+'/'
    for subdir, dirs, files in os.walk(rootdir):
        for file in dirs: 
            filepath = rootdir+file +'/features.csv' 
            if part == Participants[0]:
                features = pd.read_csv(filepath)
            else:
                features = features.append(pd.read_csv(filepath))
print 'feat'

            
            
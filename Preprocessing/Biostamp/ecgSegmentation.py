# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 18:43:00 2018

@author: zdking
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 08:11:51 2018

@author: zdking
"""

from ecgfeatures import *
import pandas as pd
import matlab.engine
import csv
import numpy as np
import os

def RRinterval(Rpeaks):
    returnArr = np.array([])
    for i in range(1,len(Rpeaks)):
        returnArr = np.append(returnArr,[Rpeaks[i]-Rpeaks[i-1]]) 
    return np.absolute(returnArr)

def CBD(durations, qrs_valid, fs):
    durations = np.array([float(x) * .0001 for x in durations])
    dur_valid = durations
    
    IQ = np.percentile(dur_valid, 75,axis = 0) - np.percentile(dur_valid, 25,axis = 0)
    QD = IQ*0.5
    MED =  3.32 * QD
    medians = np.median(dur_valid)
    MAD = float(medians - (2.9 * QD)) / 3
    CBD = float(MAD + MED) / 2
    RRk = 0
    startpos = 0
    is_valid = qrs_valid
    while startpos < len(durations) - 1:
        if qrs_valid[startpos] == 0:
            startpos = startpos + 1
        if 0.3 < durations[startpos] and durations[startpos] < 1.5:
            if abs(durations[startpos]-durations[startpos+1])<CBD:
                RRk = durations[startpos]
            else:
                is_valid[startpos] = 0
                startpos+=1
        else:
            is_valid[startpos] = 0
            startpos+=1
    for i in range(startpos+1,len(durations)):
        if qrs_valid[i]==0:
            continue
        x = durations[i]
        if 0.3<durations[i] and durations[i]<1.5:
            if is_valid[i-1]==1:
                if abs(durations[i]-durations[i-1])<=CBD:
                    is_valid[i]=1
                    RRk=durations[i]
                else:
                    is_valid[i]=0
            else:
                if abs(durations[i]-RRk)<=1.5*CBD:
                    is_valid[i]=1
                    RRk=durations[i]
                else:
                    is_valid[i]=0
        else:
            is_valid[i]=0
    return is_valid
            
def Segmentation(data, windowSize, overlap):
    winSizeMillisecond = windowSize * 1000
    stepSizeMillisecond = winSizeMillisecond * (1 - overlap)
    start_time = data['Timestamp (ms)'].iloc[0]
    end_time = data['Timestamp (ms)'].iloc[-1]

    segments_start = np.arange(start_time, end_time - winSizeMillisecond, stepSizeMillisecond)
    segments_end = segments_start + winSizeMillisecond
    
    segment = pd.DataFrame({'Start': segments_start,
                            'End': segments_end},
                           columns=['Start', 'End'])
    return segment
       
def getRpeaks(data, noiseSegment, eng):
    """getR is essentially the same as segment in wild, but with no annotations file there for the 
    are not based on the activity 
    Input:
        Participants : list of numbers that identify each participant whos features are extracted
        dataPath: file path to the ecg data 
        windowsize: size of the sliding window
        overlap: percent overlap of the sliding window
        Output: file path to where the output file is put
        
        Produces a csv file that contains all of the features for each of the participants 
    
    """    
    window = 1
    RPeaks = np.array([])
    for index, row in noiseSegment.iterrows():
        actecg = data.loc[(data['Timestamp (ms)'] >= row['Start']) 
                        & (data['Timestamp (ms)'] <= row['End'])]
        actecg.reset_index()
        x = list(actecg['Sample (V)'])
        mat_signal = matlab.double(x)[0]
        res = eng.getRpeaks(mat_signal)
        y = np.array(list(res[0]))
        y = [int(l)-1 for l in y]
        RPeaks = np.append(RPeaks,np.array(actecg.iloc[y]['Timestamp (ms)']))
    return RPeaks
  
def getECGfeatures(RPeaks, featureSegment, eng): 
    df = pd.DataFrame(columns= ['Start','End','mean',
                           'standard deviation','min','max','median','mode','skew',
                           'Kurtosis','80_percentile','60_percentile',
                           '40_percentile','20_percentile','RMS','IQR','count>mean',
                           'count<mean','range','COV_M','pNN50','pNN20','RMSSD',
                           'nn50','nn20','SDSD','zcross', 'Lf', 'MF', 'HF', 
                           'Lf/HF', 'Count'])
    for index, row in featureSegment.iterrows(): 
        start = row['Start']
        end = row['End']
        features = RPeaks[np.where((RPeaks >= start) & (RPeaks < end))]  
        rrintervals = RRinterval(features)
        mat_subdur = matlab.double(list(rrintervals))[0]
        mat_ones = matlab.double(list(np.ones(len(rrintervals))))[0]
        res = eng.CBD4(mat_subdur,mat_ones,125)
#        newres = CBD(rrintervals,np.ones(len(rrintervals)),125)
        y = np.array(list(res[0]))
        test = rrintervals * y
        if len(test) > 15:
            feat = getFeatures(test, start, end)
            ret = [start,end]
            ret = ret + feat
            df.loc[-1] = ret # adding a row
            df.index = df.index + 1  # shifting index
            df = df.sort_index()
    return df
        
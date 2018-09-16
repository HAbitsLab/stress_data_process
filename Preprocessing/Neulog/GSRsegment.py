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



def segmentNeulog(Participants, dataPath, windowSize, overlap, Output):
    """
    MUCH OF THIS WILL CHANGE WITH THE IMPLEMENTATION OF THE BACKEND
    
    Input:
        Participants : list of numbers that identify each participant whos features are extracted
        dataPath: file path to the ecg data 
        windowsize: size of the sliding window
        overlap: percent overlap of the sliding window
        Output: file path to where the output file is put"""
    windowSize = windowSize * 1000 #convert to ms
    overlap = overlap * windowSize #
    eng = matlab.engine.start_matlab()
    with open('neulogfeatures.csv', 'wb') as ec:
        writerec = csv.writer(ec)
        writerec.writerow(['Participant', 'Activity','window','mean',
                           'standar deviation','min','max','median','mode','skew',
                           'Kurtosis','80_percentile','60_percentile',
                           '40_percentile','20_percentile','RMS','IQR','count>mean',
                           'count<mean','range','COV_M','zcross', 'Lf', 'MF', 'HF', 
                           'Lf/HF', 'Count'])
        for part in Participants:#itterare through the selected participant list
            ecgfilename = dataPath + str(part) +'/elec.csv'
            anfilename = dataPath + str(part) +'/annotations.csv'
            ecg = pd.read_csv(ecgfilename)
            an = pd.read_csv(anfilename)
            for index, row in an.iterrows():#itterate through the activities in the annotations file
                startact = row['Start Timestamp (ms)']
                endact = row['Stop Timestamp (ms)']
                activity = row['EventType']
#                plt.figure()
#                plt.plot(ecg.loc[(ecg['Timestamp (ms)'] >= startact) 
#                                & (ecg['Timestamp (ms)'] <= endact)]['Sample (V)'])
#                plt.savefig('../../stress_data/participant' + str(part) +'/'+activity+'.png')
                start = startact# start is the first data point in the activity
                window = 1
                end = start + windowSize
                while start <= endact-20000:
                    actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) 
                                    & (ecg['Timestamp (ms)'] <= end)]
                    x = list(actecg['Sample (V)'])
                    mat_signal = matlab.double(x)[0]
                    res = eng.feature_min(mat_signal)
                    y = np.array(list(res[0]))
                    test = y[np.where(y>0)]
                    if len(test) > 10:
                        feat = getFeatures(y)
                        ret = [part,activity,window]
                        ret = ret + feat
                        writerec.writerow(ret)
                    window += 1
                    start = start + overlap
                    end = start + windowSize
                    if end > endact:
                        end = endact



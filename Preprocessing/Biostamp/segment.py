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


    
def segmentECG(Participants, dataPath, windowSize, overlap, Output):
    print os.path.exists(dataPath + str(Participants[0]) +'/annotations.csv')
    if os.path.exists(dataPath + str(Participants[0]) +'/annotations.csv'):
        segmentInLab(Participants, dataPath, windowSize, overlap, Output)
    else:
        segmentInWild(Participants, dataPath, windowSize, overlap, Output)
def segmentInLab(Participants, dataPath, windowSize, overlap, Output):
    windowSize = windowSize * 1000
    overlap = overlap * windowSize
    eng = matlab.engine.start_matlab()
    with open('featuresnew.csv', 'wb') as ec:
        writerec = csv.writer(ec)
        writerec.writerow(['Participant', 'Activity','window','mean',
                           'standar deviation','min','max','median','mode','skew',
                           'Kurtosis','80_percentile','60_percentile',
                           '40_percentile','20_percentile','RMS','IQR','count>mean',
                           'count<mean','range','COV_M','pNN50','pNN20','RMSSD',
                           'nn50','nn20','SDSD','zcross', 'Lf', 'MF', 'HF', 
                           'Lf/HF', 'Count'])
        for part in Participants:
            ecgfilename = dataPath + str(part) +'/elec.csv'
            if os.path.exists(dataPath + str(part) +'/annotations.csv'):
                anfilename = dataPath + str(part) +'/annotations.csv'
            ecg = pd.read_csv(ecgfilename)
            an = pd.read_csv(anfilename)
            for index, row in an.iterrows():
                startact = row['Start Timestamp (ms)']
                endact = row['Stop Timestamp (ms)']
                activity = row['EventType']
#                plt.figure()
#                plt.plot(ecg.loc[(ecg['Timestamp (ms)'] >= startact) 
#                                & (ecg['Timestamp (ms)'] <= endact)]['Sample (V)'])
#                plt.savefig('../../stress_data/participant' + str(part) +'/'+activity+'.png')
                start = startact
                window = 1
                end = start + windowSize
                while start <= endact-20000:
                    actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) 
                                    & (ecg['Timestamp (ms)'] <= end)]
                    x = list(actecg['Sample (V)'])
#                    with open('noise.csv', 'wb') as f:
#                        writer = csv.writer(f)
#                        for val in x:
#                            writer.writerow([val])
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

def segmentInWild(Participants, dataPath, windowSize, overlap, Output):
    windowSize = windowSize * 1000
    overlap = overlap * windowSize
    eng = matlab.engine.start_matlab()
    with open(Output + 'InWildfeaturesp3.csv', 'wb') as ec:
        writerec = csv.writer(ec)
        writerec.writerow(['Participant', 'Start','End','window','mean',
                           'standar deviation','min','max','median','mode','skew',
                           'Kurtosis','80_percentile','60_percentile',
                           '40_percentile','20_percentile','RMS','IQR','count>mean',
                           'count<mean','range','COV_M','pNN50','pNN20','RMSSD',
                           'nn50','nn20','SDSD','zcross', 'Lf', 'MF', 'HF', 
                           'Lf/HF', 'Count'])
        for part in Participants:   
            print part
            rootdir = dataPath+str(part)+'/'
            for subdir, dirs, files in os.walk(rootdir):
                for file in dirs: 
                    print file
                    filepath = rootdir+file +'/elec.csv' 
                    ecg = pd.read_csv(filepath)
                    firstrow = ecg.iloc[0]
                    lastrow = ecg.iloc[len(ecg)-1]
                    startact = firstrow['Timestamp (ms)']
                    endact = lastrow['Timestamp (ms)']
                    start = startact
                    window = 1
                    end = start + windowSize
                    while start <= endact-20000:
                        actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) 
                                        & (ecg['Timestamp (ms)'] <= end)]
                        x = list(actecg['Sample (V)'])
#                        with open('noise.csv', 'wb') as f:
#                            writer = csv.writer(f)
#                            for val in x:
#                                writer.writerow([val])
                        mat_signal = matlab.double(x)[0]
                        res = eng.feature_min(mat_signal)
                        y = np.array(list(res[0]))
                        test = y[np.where(y>0)]
                        if len(test) > 10:
                            feat = getFeatures(y)
                            ret = [part,start,end,window]
                            ret = ret + feat
                            writerec.writerow(ret)
                        window += 1
                        start = start + overlap
                        end = start + windowSize
                        if end > endact:
                            end = endact
                    


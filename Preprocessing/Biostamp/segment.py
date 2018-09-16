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
       
        
    
def segmentECG(Participants, dataPath, windowSize, overlap, Output):
    
    print os.path.exists(dataPath + str(Participants[0]) +'/annotations.csv')
    if os.path.exists(dataPath + str(Participants[0]) +'/annotations.csv'):
        #If there exists an annotations file then the data contains activities
        segmentInLab(Participants, dataPath, windowSize, overlap, Output)
    else:
        segmentInWild(Participants, dataPath, windowSize, overlap, Output)
def segmentInLab(Participants, dataPath, windowSize, overlap, Output):
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
    with open('featuresnew.csv', 'wb') as ec:
        writerec = csv.writer(ec)
        writerec.writerow(['Participant', 'Activity','window','mean',
                           'standar deviation','min','max','median','mode','skew',
                           'Kurtosis','80_percentile','60_percentile',
                           '40_percentile','20_percentile','RMS','IQR','count>mean',
                           'count<mean','range','COV_M','pNN50','pNN20','RMSSD',
                           'nn50','nn20','SDSD','zcross', 'Lf', 'MF', 'HF', 
                           'Lf/HF', 'Count'])
        for part in Participants:#itterare through the selected participant list
            print part
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
                RPeaks = np.array([])
                while start <= endact-20000:
                    actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) 
                                    & (ecg['Timestamp (ms)'] <= end)]
                    x = list(actecg['Sample (V)'])
                    mat_signal = matlab.double(x)[0]
                    res = eng.getRpeaks(mat_signal)
                    y = np.array(list(res[0]))
                    RPeaks = np.append(RPeaks,y)
                mat_subdur = matlab.double(y)[0]
                mat_ones = matlab.double(np.ones(len(y)))[0]
                res = eng.CBD4(mat_subdur,mat_ones,125)
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
    print 'Wild'
    """segmentInWild is essentially the same as segment in wild, but with no annotations file there for the 
    are not based on the activity 
    Input:
        Participants : list of numbers that identify each participant whos features are extracted
        dataPath: file path to the ecg data 
        windowsize: size of the sliding window
        overlap: percent overlap of the sliding window
        Output: file path to where the output file is put
        
        Produces a csv file that contains all of the features for each of the participants 
    
    """
    windowSize = windowSize * 1000 #convert to ms
    overlap = overlap * windowSize
    eng = matlab.engine.start_matlab()
    with open(Output + 'InWildfeaturesall8-16.csv', 'wb') as ec:
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
            print rootdir
            for subdir, dirs, files in os.walk(rootdir):
                print dirs
                for file in dirs: 
                    print file
                    filepath = rootdir+file +'/elec.csv' 
                    ecg = pd.read_csv(filepath)
                    noiseSegment = Segmentation(ecg, 60, 0)
                    featureSegment = Segmentation(ecg, windowSize, overlap)
                    firstrow = ecg.iloc[0]
                    lastrow = ecg.iloc[len(ecg)-1]
                    startact = firstrow['Timestamp (ms)']
                    endact = lastrow['Timestamp (ms)']
                    start = startact
                    window = 1
                    end = start + windowSize
                    RPeaks = np.array([])
                    while start <= endact-20000:
                        actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) 
                                        & (ecg['Timestamp (ms)'] <= end)]
                        actecg.reset_index()
                        x = list(actecg['Sample (V)'])
                        mat_signal = matlab.double(x)[0]
                        res = eng.getRpeaks(mat_signal)
                        y = np.array(list(res[0]))
                        y = [int(l)-1 for l in y]
                        RPeaks = np.append(RPeaks,np.array(actecg.iloc[y]['Timestamp (ms)']))
                        start = start + windowSize
                        end = start + windowSize
                    
                    
                    mat_subdur = matlab.double(RRinterval(y))[0]
                    mat_ones = matlab.double(np.ones(len(y)))[0]
                    res = eng.CBD4(mat_subdur,mat_ones,125)
                    y = np.array(list(res[0]))
                    print y
                    test = y[np.where(y>0)]
                    if len(test) > 10:
                        feat = getFeatures(y)
                        ret = [part,start,end,window]
                        print ret
                        ret = ret + feat
                    writerec.writerow(ret)
                    window += 1
                    start = start + overlap
                    end = start + windowSize
                    if end > endact:
                        end = endact
                    


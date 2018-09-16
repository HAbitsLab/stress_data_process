# -*- coding: utf-8 -*-
"""
Created on Sat Jun 09 00:28:26 2018

@author: zdking
"""

import pandas as pd
import numpy as np
from scipy import stats
import scipy.fftpack
import math
import matplotlib.pyplot as plt

def getFreq(data):
    fourier = scipy.fftpack.fft(data)
    n = data.size
    fourier = abs(data/n)
    freq = scipy.fftpack.fftfreq(n)
    Low = 0
    Med = 0
    Hi = 0
    i = 0
    for val in freq:
        if val >= 0.1 and val < 0.2:
            Low = Low + fourier[i]
        if val >= 0.2 and val < 0.3:
            Med = Med + fourier[i]
        if val >= 0.3 and val < 0.4:
            Hi = Hi + fourier[i]
        i += 1
    return [Low, Med, Hi]

def diffRR(data):
    i = 0
    flag = 0
    dif  = np.array([])
    for val in data:
         if flag > 0:
             if data[i] > 0:
                 dif = np.append(dif,abs(val-data[i-1]))
             else:
                 flag = -1
         flag += 1        
         i += 1 
    return dif

def calcFFT(y):
    # TEST CASE:
    # >>>print(calc_fft(np.array([1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1,2,3,4,5,4,3]), 16))
    # output:
    # >>>[ 0.10867213  0.22848475  1.67556733  0.1980655   0.11177658  0.08159451
    # 0.07137028  0.12458543  0.26419639  0.10726005]

    # Number of samplepoints
    N = y.shape[0]

    yf = scipy.fftpack.fft(y)
    amp = 2.0/N * np.abs(yf[:int(N/2)])

    return amp

def convertHR(data):
    HR = np.array([])
    for val in data:
        HR = np.append(HR,(60000/float(val))+1)
    return HR
    
def zeroCross(data):
    i = 0
    cnt = 0
    mean = np.mean(data,axis = 0)
    for val in data:
         if i >0:
             if ((data[i] > mean) and (data[i-1] < mean)) or ((data[i] < mean) and (data[i-1] > mean)):
                 cnt += 1
         i += 1 
    return cnt

def getFeatures(data):
     data = data[np.where(data>0)]
     minFloat = np.amin(data,axis = 0)
     maxFloat = np.amax(data,axis = 0)
     meanFloat = np.mean(data,axis = 0)
     medianFloat = np.median(data,axis =0)
     modeFloat = stats.mode(data, axis = 0)
     sdFloat = np.std(data,axis = 0)
     skewFloat = stats.skew(data,axis = 0)
     kurFloat = stats.kurtosis(data,axis = 0)
     eightperFloat = np.percentile(data, 80,axis = 0)
     sixperFloat = np.percentile(data, 60,axis = 0)
     fourperFloat = np.percentile(data, 40,axis = 0)
     twoperFloat = np.percentile(data, 20,axis = 0)
     rmsFloat = np.sqrt(np.mean(data**2))
     iqrFloat = stats.iqr(data,axis = 0)
     countgeqInt = len(np.where( data > meanFloat)[0])/float(len(data))
     countleqInt = len(np.where( data < meanFloat)[0])/float(len(data))
     rangFloat = maxFloat - minFloat
     [LfFloat, MFFloat, HFFloat] = getFreq(data)
     COV_MFloat = np.cov(data.T)
     zcrossInt = zeroCross(data)
     
     
     #HR = convertHR(data)
     CountInt = len(data)
     return [meanFloat,sdFloat,minFloat,maxFloat,medianFloat,modeFloat,skewFloat,
             kurFloat,eightperFloat,sixperFloat,fourperFloat,twoperFloat,rmsFloat,
             iqrFloat,countgeqInt,countleqInt,rangFloat,COV_MFloat,zcrossInt, LfFloat,
             MFFloat, HFFloat, LfFloat/HFFloat, CountInt]
 
#eng = matlab.engine.start_matlab()
#with open('featuresnew.csv', 'wb') as ec:
#    writerec = csv.writer(ec)
#    writerec.writerow(['Participant', 'Activity','window','mean',
#                       'standar deviation','min','max','median','mode','skew',
#                       'Kurtosis','80_percentile','60_percentile',
#                       '40_percentile','20_percentile','RMS','IQR','count>mean',
#                       'count<mean','range','COV_M','pNN50','pNN20','RMSSD',
#                       'nn50','nn20','SDSD','zcross', 'Lf', 'MF', 'HF', 
#                       'Lf/HF', 'Count'])
#    for part in [2,3,4,6,7,9,11,13,14,15,16,17,20,21,22]:
#        print part
#        ecgfilename = '../../stress_data/participant' + str(part) +'/elec.csv'
#        anfilename = '../../stress_data/participant' + str(part) +'/annotations.csv'
#        ecg = pd.read_csv(ecgfilename)
##    Timestamp (ms)	Sample (V)
#        an = pd.read_csv(anfilename)
##        EventType	Start Timestamp (ms)	Stop Timestamp (ms)
#        for index, row in an.iterrows():
#            startact = row['Start Timestamp (ms)']
#            endact = row['Stop Timestamp (ms)']
#            activity = row['EventType']
#            plt.figure()
#            plt.plot(ecg.loc[(ecg['Timestamp (ms)'] >= startact) 
#                            & (ecg['Timestamp (ms)'] <= endact)]['Sample (V)'])
#            plt.savefig('../../stress_data/participant' + str(part) +'/'+activity+'.png')
#            start = startact
#            window = 1
#            end = start + 60000
#            while start <= endact-20000:
#                actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) 
#                                & (ecg['Timestamp (ms)'] <= end)]
#                x = list(actecg['Sample (V)'])
#                with open('noise.csv', 'wb') as f:
#                    writer = csv.writer(f)
#                    for val in x:
#                        writer.writerow([val])
#                mat_signal = matlab.double(x)[0]
#                res = eng.feature_min()
#                y = np.array(list(res[0]))
#                test = y[np.where(y>0)]
#                if len(test) > 10:
#                    feat = getfeatures(y)
#                    ret = [part,activity,window]
#                    ret = ret + feat
#                    writerec.writerow(ret)
#                window += 1
#                start = start + 30000
#                end = start + 60000
#                if end > endact:
#                    end = endact
#                
                
                
                
        



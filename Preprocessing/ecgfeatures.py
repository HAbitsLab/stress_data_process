# -*- coding: utf-8 -*-
"""
Created on Sat Jun 09 00:28:26 2018

@author: zdking
"""

import pandas as pd
import matlab.engine
import csv
import numpy as np
from scipy import stats
import scipy.fftpack
import math

def getfreq(data):
    fourier = np.fft.fft(data)
    n = data.size
    timestep = 0.004
    freq = np.fft.fftfreq(n, d=timestep)
    return freq
def diff(data):
    i = 0
    dif  = np.array([])
    for val in data:
         if i >0:
             dif = np.append(dif,abs(val-data[i-1]))
         i += 1 
    return dif

def calc_fft(y):
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


def getfeatures(data):
     min = np.amin(data,axis = 0)
     max = np.amax(data,axis = 0)
     mean = np.mean(data,axis = 0)
     median = np.median(data,axis =0)
     sd = np.std(data,axis = 0)
     skew = stats.skew(data,axis = 0)
     kur = stats.kurtosis(data,axis = 0)
     eightper = np.percentile(data, 80,axis = 0)
     sixper = np.percentile(data, 60,axis = 0)
     fourper = np.percentile(data, 40,axis = 0)
     twoper = np.percentile(data, 20,axis = 0)
     rms = np.sqrt(np.mean(data**2))
     iqr = stats.iqr(data,axis = 0)
     countgeq = len(np.where( data > mean)[0])/float(len(data))
     countleq = len(np.where( data < mean)[0])/float(len(data))
     rang = max - min
     freq = calc_fft(data)
     COV_M = np.cov(data.T)
     dif = diff(data)
     pNN50 = len(np.where(dif>50))/float(len(data))
     pNN20 = len(np.where(dif>20))/float(len(data))
     RMSSD = math.sqrt(np.mean(dif*dif))
     return [mean,sd,min,max,median,skew,kur,eightper,sixper,fourper,twoper,rms,
             iqr,countgeq,countleq,rang,freq,COV_M,pNN50,pNN20,SDSD]
 
eng = matlab.engine.start_matlab()
for part in [2,3,4,6,7,9,11,13,14,15,16,17,20,21,22]:
    print part
    ecgfilename = 'stress_data/participant' + str(part) +'/elec.csv'
    anfilename = 'stress_data/participant' + str(part) +'/annotations.csv'
    ecg = pd.read_csv(ecgfilename)
#    Timestamp (ms)	Sample (V)
    an = pd.read_csv(anfilename)
#    EventType	Start Timestamp (ms)	Stop Timestamp (ms)
    for index, row in an.iterrows():
        startact = row['Start Timestamp (ms)']
        endact = row['Stop Timestamp (ms)']
        activity = row['EventType']
        start = startact
        end = start + 60000
        while start <= endact-20000:
            actecg = ecg.loc[(ecg['Timestamp (ms)'] >= start) & (ecg['Timestamp (ms)'] <= end)]
            x = list(actecg['Sample (V)'])
            with open('noise.csv', 'wb') as f:
                writer = csv.writer(f)
                for val in x:
                    writer.writerow([val])
            mat_signal = matlab.double(x)[0]
            res = eng.feature_min()
            y = np.array(list(res[0]))
            feat = getfeatures(y)
            print feat
            start = start + 30000
            end = start + 60000
            if end > endact:
                end = endact
            
            
            
            
        



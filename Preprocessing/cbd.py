# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 16:06:04 2018

@author: zdking
"""
import numpy as np

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
                
            
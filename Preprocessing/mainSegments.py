# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 18:59:22 2018

@author: zdking
"""
from Biostamp import ecgSegmentation
import label_to_segment
import pandas as pd
import matlab.engine
import numpy as np
import os

Participants = ['participant2','participant3','participant4','participant6',
                'participant7','participant9','participant10','participant11',
                'participant13','participant14','participant15','participant16',
                'participant17','participant18','participant19','participant20',
                'participant21','participant22']#participant identifiers
dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/stress_data/'
#dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/Tech_Pilot1/ECG_Accel/' #location of stress data
Output = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/output/'
#Participants = ['0007'] #participant identifiers
#dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/MB_intervention/'
#dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/Tech_Pilot1/ECG_Accel/' #location of stress data
#Output = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/Tech_Pilot1/Output/'
windowSize = 60 # In seconds
overlap = 0.5 # percent window overlap
eng = matlab.engine.start_matlab()
for part in Participants:   
    rootdir = dataPath+str(part)
    
    
    filepath = rootdir+'/elec.csv' 
    print filepath
    ecg = pd.read_csv(filepath)
    noiseSegment = ecgSegmentation.Segmentation(ecg, 60, 0)
    featureSegment = ecgSegmentation.Segmentation(ecg, windowSize, overlap)
    Rpeaks = np.array(ecgSegmentation.getRpeaks(ecg, noiseSegment, eng))
    print Rpeaks
    daysData = ecgSegmentation.getECGfeatures(Rpeaks, featureSegment, eng)
    daysData.to_csv(rootdir + '/features.csv')
    
    
#    for subdir, dirs, files in os.walk(rootdir):
#        for file in dirs: 
#            filepath = rootdir+file +'/elec.csv' 
#            print filepath
#            ecg = pd.read_csv(filepath)
#            noiseSegment = ecgSegmentation.Segmentation(ecg, 60, 0)
#            featureSegment = ecgSegmentation.Segmentation(ecg, windowSize, overlap)
#            Rpeaks = np.array(ecgSegmentation.getRpeaks(ecg, noiseSegment, eng))
#            print Rpeaks
#            daysData = ecgSegmentation.getECGfeatures(Rpeaks, featureSegment, eng)
#            daysData.to_csv(rootdir + file + '/features.csv')


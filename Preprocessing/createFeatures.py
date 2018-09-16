# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:14:55 2018

@author: zdking"""
from Biostamp import segment

Participants = ['participant2','participant3','participant4','participant6',
                'participant7','participant9','participant10','participant11',
                'participant13','participant14','participant15','participant16',
                'participant17','participant18','participant19','participant20',
                'participant21','participant22']#participant identifiers
dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/stress_data/'
#dataPath = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/Tech_Pilot1/ECG_Accel/' #location of stress data
Output = 'C:/Users/zdking/Habitslab/stress_data_process/stress_data_process/output/'
windowSize = 60 # In seconds
overlap = 0.5 # percent window overlap
segment.segmentECG(Participants, dataPath, windowSize, overlap, Output)

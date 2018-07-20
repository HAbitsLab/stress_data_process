# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:14:55 2018

@author: zdking"""
from Biostamp import segment

Participants = ['p3'] #participant identifiers
dataPath = 'E:/COLLEGE_STUDENT_STRESS/cleaning/infield/' #location of stress data
Output = 'E:/COLLEGE_STUDENT_STRESS/output/'
windowSize = 60 # In seconds
overlap = 0.5 # percent window overlap
segment.segmentECG(Participants, dataPath, windowSize, overlap, Output)

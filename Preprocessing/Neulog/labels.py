# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 13:35:07 2018

@author: zdking
"""
import pandas as pd
import numpy as np

def getThreshold(label):
    mean = sum(label)/float(len(label))
    returnArr = np.array([])
    for x in label:
        if x >= mean:
            returnArr = np.append(returnArr, 1)
        else:
            returnArr = np.append(returnArr, 0)
    return returnArr

def getLabel(participant):
    dataPathStr = '../../Tech_Pilot1/RedCap/'+participant + '/'
    emaDF = pd.read_csv(dataPathStr+'EMA.csv')
    microDF = pd.read_csv(dataPathStr+'Micro-EMA.csv')
    emaHeadersArr = ['BinaryStress',
               'LikertStress',
               'PSS-Control',
               'PSS-Confident',
               'PSS-YourWay',
               'PSS-Overcome',
               'HappyStress',
               'ExcitedStress',
               'ContentStress',
               'WorriedStress'
               'IrritableStress',
               'SadStress']
    emaDefsDF = emaDF.iloc[:,0:11]
    emaDefsDF.columns = emaHeadersArr
    BinaryStress = np.array(list(emaDefsDF['BinaryStress']))
    labeldic = {}
    for x in emaDefsDF.columns:
        temp = list(emaDefsDF[x])
        StressDef = getThreshold(temp)
        labeldic.update{{x:StressDef}}
    PSS-Q4 = np.array([])   
    Control = emaDefsDF['PSS-Control']
    Confident = emaDefsDF['PSS-Confident']
    YourWay = emaDefsDF['PSS-YourWay']
    Overcome = emaDefsDF['PSS-Overcome']
    for x in len(Control):
        pss = Control[x] + Overcome[x] - Confident[x] - YourWay[x]
        if pss  >= 4.7:
            np.append(PSS-Q4,1)
        else:
            np.append(PSS-Q4,0)
    
        
#    PSS-Control = getThreshold(list(emaDefsDF['How stressed were you feeling?']))
#    PSS-Confident = getThreshold(emaDefsDF['How stressed were you feeling?'])
#    PSS-YourWay = getThreshold(emaDefsDF['How stressed were you feeling?'])
#    PSS-Overcome = getThreshold(emaDefsDF['How stressed were you feeling?'])
#    HappyStress = getThreshold(emaDefsDF['How happy were you feeling?'])
#    ExcitedStress = getThreshold(emaDefsDF['How excited were you feeling?'])
#    ContentStress = getThreshold(emaDefsDF['How content were you feeling?'])
#    WorriedStress = getThreshold(emaDefsDF['How worried were you feeling?'])
#    IrritableStress = getThreshold(emaDefsDF['How irritable/angry were you feeling?'])
#    SadStress = getThreshold(emaDefsDF['How sad were you feeling?'])
    
    
getLabel('101')
    
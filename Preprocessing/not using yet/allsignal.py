import csv
import os
import numpy
import matplotlib.pyplot as plt

for filename in os.listdir('stress_data'):
    filename = 'participant2'
    with open('stress_data/' + filename + '/elec.csv','rb') as ecg:
        reader = csv.reader(ecg)
        ecglist = list(reader)
        listlen = len(ecglist)
        rowInt = 0
        time = numpy.zeros(listlen-1)
        sample = numpy.zeros(listlen-1)
        for row in ecglist:
            if rowInt != 0:
                time[rowInt-1] = float(row[0])
                sample[rowInt-1] = float(row[1])
            rowInt+=1
        print len(time)
        plt.plot(time,sample,color = 'red')
        plt.show()

def checkannotations(time,filename):
    with open('stress_data/'+filename+ '/annotations.csv', 'rb') as annotation:
        reader = csv.reader(annotation)
        annlist = list(reader)
        

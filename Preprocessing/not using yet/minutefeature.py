import csv
import numpy
import os
from scipy import stats
import sys
def getfeatures(name,data,wind):
     min = numpy.amin(data,axis = 0)
     max = numpy.amax(data,axis = 0)
     mean = numpy.mean(data,axis = 0)
     median = numpy.median(data,axis =0)
     sd = numpy.std(data,axis = 0)
     skew = stats.skew(data,axis = 0)
     kur = stats.kurtosis(data,axis = 0)
     per = numpy.percentile(data, 80,axis = 0)
     tper = numpy.percentile(data, 20,axis = 0)
     x = {wind : [name,mean,sd,min,max,median,skew,kur,per,tper,wind]}
     return x

f = {}
totalfeatures = {}
seg = int(sys.argv[1]) #20000
overlap = seg * float(sys.argv[2])
device = sys.argv[3] #polar/ neulog
timeind = int(sys.argv[4])#5
dataind = int(sys.argv[5]) #3
for part in os.listdir('stress_data'):# each participant has a file 
    with open('stress_data/'+part+ '/annotations.csv', 'rb') as annotation:
        reader = csv.reader(annotation)
        rowInt = 0
        Start ="NA"
        End = "NA"
        f ={}
        for row in reader:
            x = {}
            if rowInt != 0:
                Start = int(row[4])
                End = int(row[5])
                Event = row[2]
                x = {Event : [Start,End]}
                f.update(x)
            rowInt += 1
    p = {part : f}
    for filename in os.listdir('stress_data/' + part + '/' + device):
        f ={}
        print filename
        iteration = 1
        with open('stress_data/'+part+'/'+device + '/' +filename) as HRdata:
            reader = csv.reader(HRdata)
            name =  filename[len(device) + 1:len(filename)-4]#remove the device name, underscore and '.csv' from the filename
            start = int(p[part][name][0])
            nxtstart = int(p[part][name][0]) + overlap
            end = int(p[part][name][0]) + seg
            rowInt = 0
            data = numpy.array([])
            nxtdata = numpy.array([])
            for row in reader:
                if rowInt != 0:
                    if int(row[timeind]) > nxtstart:
                        nxtdata = numpy.append(nxtdata, float(row[dataind]))
                    if int(row[timeind]) < end:
                        if int(row[timeind]) > start:
                            data = numpy.append(data, float(row[dataind]))
                    else:
                        features = getfeatures(name,data,iteration)
                        iteration += 1
                        f.update(features)
                        start = nxtstart
                        end = start + seg
                        nxtstart = start + overlap
                        data = nxtdata
                        nxtdata = numpy.array([])
                        nxtdata = numpy.append(nxtdata, float(row[dataind]))
                rowInt += 1
            f.update(getfeatures(name,data,iteration))
            totalfeatures.update({filename: f})
    with open('stress_data/' + part + '/'+device + 'feature.csv', 'wb') as feature:
        writer = csv.writer(feature)
        writer.writerow(['activity','mean','standard deviation','min','max','median','skew','kurtosis','80_percentile','20_percentile','window_number'])
        for v in totalfeatures:
            for val in totalfeatures[v]:
                writer.writerow(totalfeatures[v][val])


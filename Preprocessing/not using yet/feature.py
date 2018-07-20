import csv
import numpy
import os
from scipy import stats
f = {}
participant = 'participant13'
check = 'neulog'
for filename in os.listdir('stress_data/' + participant+'/'+check):
    with open('stress_data/'+participant+'/'+filename) as HRdata:
        reader = csv.reader(HRdata)
        rnewreader = list(reader)
        nrows = len(rnewreader)
        rowInt = 0
        data = numpy.array([])
        odata = numpy.array([])
        num = 0
        flag = 0
        oflag = 0
        for row in rnewreader:
            if rowInt != 0:
                colInt = 0
                for col in row:
                    if flag == 0 and colInt == 2:
                        flag = 1
                        oflag = 1
                        start = int(row[2])      
                    if flag == 1:
                        if colInt == 1:
                            data = numpy.append(data, float(col))
                        if colInt == 2:
                            if (int(col) - start) >= 20000 or rowInt == nrows-1:
                                    flag = 2
                                    end = int(col)
                                    num += 1           
                    if oflag == 1:
                        if colInt == 2:
                            if (int(col) - start) >= 10000:
                                ostart = start + 10000
                                oflag = 2
                    if oflag == 2:
                        if colInt == 1:
                            odata = numpy.append(odata, float(col))
                    colInt += 1
                    if flag == 2:
                        min = numpy.amin(data,axis = 0)
                        max = numpy.amax(data,axis = 0)
                        mean = numpy.mean(data,axis = 0)
                        median = numpy.median(data,axis =0)
                        sd = numpy.std(data,axis = 0)
                        skew = stats.skew(data,axis = 0)
                        kur = stats.kurtosis(data,axis = 0)
                        per = numpy.percentile(data, 80,axis = 0)
                        tper = numpy.percentile(data, 20,axis = 0)
                        name = filename + str(num)
                        x = {name : [filename,num,mean,sd,min,max,median,skew,kur,per,tper,start,end,start-end]}
                        f.update(x)
                        start = ostart
                        flag = 1
                        data = odata
                        odata = numpy.array([])
                        oflag = 1
                        if rowInt == nrows:
                            min = numpy.amin(data,axis = 0)
                            max = numpy.amax(data,axis = 0)
                            mean = numpy.mean(data,axis = 0)
                            median = numpy.median(data,axis =0)
                            sd = numpy.std(data,axis = 0)
                            skew = stats.skew(data,axis = 0)
                            kur = stats.kurtosis(data,axis = 0)
                            per = numpy.percentile(data, 80,axis = 0)
                            tper = numpy.percentile(data, 20,axis = 0)
                            name = filename + str(num+1)
                            print filename
                            x = {name : [filename,num+1,mean,sd,min,max,median,skew,kur,per,tper]}
                            f.update(x)
            rowInt += 1
with open('stress_data/send/'+check+'feat2.csv', 'wb') as feature:
    writer = csv.writer(feature)
    for val in f:
       
        writer.writerow(f[val])

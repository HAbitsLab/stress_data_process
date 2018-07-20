import csv
import numpy
import os
from scipy import stats
f = {}
device = 'polar'
for part in os.listdir('stress_data'):
    for filename in os.listdir('stress_data/' + part + '/' + device):
        with open('stress_data/'+part+'/'+device + '/' +filename) as HRdata:
            reader = csv.reader(HRdata)
            rowInt = 0
            min = 200
            max = 0
            sum = 0
            countInt = 0
            data = numpy.array([])
            for row in reader:
                if rowInt != 0:
                    colInt = 0
                    for col in row:
                        if colInt == 3:
                            print col
                            sum += float(col)
                            countInt += 1
                            data = numpy.append(data, float(col))
                            if float(col) > max:
                                max = float(col)
                            if float(col) < min:
                                if float(col) > 20:
                                    min = float(col)
                        colInt += 1
                rowInt += 1
            min = numpy.amin(data,axis = 0)
            max = numpy.amax(data,axis = 0)
            mean = numpy.mean(data,axis = 0)
            median = numpy.median(data,axis =0)
            sd = numpy.std(data,axis = 0)
            skew = stats.skew(data,axis = 0)
            kur = stats.kurtosis(data,axis = 0)
            per = numpy.percentile(data, 80,axis = 0)
            tper = numpy.percentile(data, 20,axis = 0)
            x = {filename : [filename,mean,sd,min,max,median,skew,kur,per,tper]}
            f.update(x)
    print f
    with open('stress_data/' + part + '/'+device + 'feature.csv', 'wb') as feature:
        writer = csv.writer(feature)
        for val in f:
            writer.writerow(f[val])
    
                

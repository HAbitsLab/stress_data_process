import csv
import numpy
import os
f = {}

for part in os.listdir('stress_data'):
    for filename in os.listdir('stress_data/' + part):
        if 'polar_' in filename:
            with open('stress_data/'+part+'/'+filename) as HRdata:
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
                mean = sum/countInt
                sd = numpy.std(data,axis = 0)
                x = {filename : [filename,mean,sd,min,max]}
                f.update(x)
    print f
    with open('stress_data/' + part + '/polarfeature.csv', 'wb') as feature:
        writer = csv.writer(feature)
        for val in f:
            writer.writerow(f[val])
    
                

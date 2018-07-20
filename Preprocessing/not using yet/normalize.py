import csv
import numpy
import os

def writedata(part, device, minmax):
    with open('stress_data/' + part + '/'+device + 'feature.csv') as data:
        reader = csv.reader(data)
        with open('stress_data/' + part + '/normalized'+device + 'feature.csv','wb') as feature:
            writer = csv.writer(feature)
            writer.writerow(['activity','mean','standard deviation','min','max','median','skew','kurtosis','80_percentile','20_percentile','window_number'])
            rowint = 0
            for row in reader:
                newrow = row
                if rowint != 0:
                    if 'cry-rest' in row[0] or 'NA' in row[0] or 'Rest- TSST' in row[0]:
                        print row[0]
                    else:
                        for i in range(1,len(row)-1):
                            newrow[i] = (float(row[i])-minmax[i][0])/(minmax[i][1] -minmax[i][0])
                        writer.writerow(newrow)
                        
                rowint+=1
devices = ['neulog','polar']
#for part in os.listdir('stress_data'):# each participant has a file
for part in ["participant20","participant21","participant22"]:
    for device in devices:
        minmax = {}
        with open('stress_data/' + part + '/'+device + 'feature.csv') as data:
            reader = csv.reader(data)
            rowint = 0
            read = list(reader)
            print len(read)
            for row in read:
                if rowint == 0:
                    totalfeatures = numpy.zeros([len(read)-1,len(row)-2])
                else:
                    for i in range(1,len(row)-1):
                        val = float(row[i])
                        totalfeatures[rowint-1][i-1] = val
                        if i in minmax:
                            if minmax[i][0] > val:
                                minmax[i][0] = val
                            if minmax[i][1] < val:
                                minmax[i][1] = val
                        else:
                            minmax.update({i : [val,val]})    
                        
                rowint += 1
        writedata(part,device,minmax)
            

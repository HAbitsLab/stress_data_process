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
     x = {wind : [mean,sd,min,max,median,skew,kur,per,tper,wind]}
     return x

def findactivity(time, dicti,part):
     for val in dicti[part]:
          if int(time) >= dicti[part][val][0] and int(time) < dicti[part][val][1]:
               return val
          
     return 'none'

def builddict():
     p = {}
     #for part in os.listdir('stress_data'):# each participant has a file
     for part in ["participant6"]:
          with open('stress_data/'+part+ '/annotations.csv', 'rb') as annotation:
               reader = csv.reader(annotation)
               rowInt = 0
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
               p.update({part : f})
     return p
totalfeatures = {}
p = builddict()
#for part in os.listdir('stress_data'):# each participant has a file
for part in ["participant6"]:
     print part
     seg = int(sys.argv[1]) #20000
     overlap = seg * float(sys.argv[2])
     device = sys.argv[3] #polar/ neulog
     timeind = int(sys.argv[4])#5
     dataind = int(sys.argv[5]) #3
     f ={}
     iteration = 1
     with open('stress_data/'+part+'/'+device + '.csv') as HRdata:
          reader = csv.reader(HRdata)
          start = 'NA'
          nxtstart = 'NA'
          end = 'NA'
          name = 'NA'
          rowInt = 0
          data = numpy.array([])
          nxtdata = numpy.array([])
          for row in reader:
               if rowInt != 0:
                    if name in 'NA':
                         if not row[timeind]:
                              continue
                         val = findactivity(row[timeind],p,part)
                         if val not in 'none':
                              start = p[part][val][0]
                              end = p[part][val][0] + seg
                              endact = p[part][val][1]
                              name = val
                              nxtstart = start + overlap
                              iteration = 1
                              f ={}
                         else:
                              continue
                    else:
                         if int(row[timeind]) > endact:
                              if iteration < 10:
                                   f.update(getfeatures(name,data,iteration))
                              val = findactivity(int(row[timeind]),p,part)
                              totalfeatures.update({name: f})
                              if val not in 'none':
                                   name = val
                                   start = p[part][val][0]
                                   end = p[part][val][0] + seg
                                   endact = p[part][val][1]
                                   nxtstart = start + overlap
                                   iteration = 1
                                   f ={}
                              else:
                                   start = 'NA'
                                   nxtstart = 'NA'
                                   end = 'NA'
                                   name = 'NA'
                                   continue
                         if int(row[timeind]) > nxtstart:
                              #if float(row[dataind]) > 10:
                              #else:
                              nxtdata = numpy.append(nxtdata, float(row[dataind]))
                         if int(row[timeind]) < end:
                              if int(row[timeind]) > start:
                                   #if float(row[dataind]) > 10:
                                   #    print 
                                   #else:
                                   data = numpy.append(data, float(row[dataind]))
                         else:
                              features = getfeatures(name,data,iteration)
                              if iteration > 9:
                                   print iteration
                              f.update(features)
                              iteration += 1
                              start = nxtstart
                              end = start + seg
                              nxtstart = start + overlap
                              data = nxtdata
                              nxtdata = numpy.array([])
                              nxtdata = numpy.append(nxtdata, float(row[dataind]))     
               rowInt += 1
          totalfeatures.update({name: f})
     with open('stress_data/' + part + '/'+device + 'feature.csv', 'wb') as feature:
          writer = csv.writer(feature)
          writer.writerow(['activity','mean','standard deviation','min','max','median','skew','kurtosis','80_percentile','20_percentile','window_number'])
          for v in totalfeatures:
               for val in totalfeatures[v]:
                    writer.writerow(numpy.append([v],totalfeatures[v][val]))


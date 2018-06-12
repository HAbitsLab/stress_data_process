import csv
import time
participant = 'participant13'
device = 'neulog'
with open('stress_data/'+participant+'/'+device+'.csv','rU') as gsr:
    readgs = csv.reader(gsr)
    rowgs = readgs.next()
    with open('stress_data/'+participant+'/annotations.csv') as ann:
        readann = csv.reader(ann)
        rownum = 0
        for row in readann:
            print 1
            event = []
            colnum = 0
            if rownum != 0:
                for col in row:
                    if colnum == 1:
                        name = col
                        print name
                    if colnum == 4:
                        start = col
                    if colnum == 5:
                        end = col
                    colnum +=1
                flag = 0
                while flag != 2:
                    print rowgs = readgs.next()
                    colnumgsr = 0
                    for colgsr in rowgs:
                        if colnumgsr == 5:
                            if flag == 0:
                                if colgsr >= start:
                                    flag = 1
                            else:
                                if colgsr >= end:
                                    flag = 2
                        colnumgsr += 1
                    if flag == 1:
                        event.append(rowgs)
                    
                with open('stress_data/'+participant+'/'+device+'/polar_' + name + '.csv', 'wb') as newfile:
                    writer = csv.writer(newfile)
                    for val in event:
                        writer.writerow(val)
            rownum += 1
            
                    
                    

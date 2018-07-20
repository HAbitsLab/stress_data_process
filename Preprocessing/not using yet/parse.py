import os
import csv
num =0
"""for filename in os.listdir('stress_data'):"""
filename = 'participant22'
device = 'elec'
with open('stress_data/'+filename+ '/annotations.csv', 'rb') as annotation:
    reader = csv.reader(annotation)
    rowInt = 0
    Start ="NA"
    End = "NA"
    f ={}
    for row in reader:
        x = {}
        if rowInt != 0:
            Start = row[4]
            End = row[5]
            Event = row[2]
            x = {Event : [Start,End]}
        f.update(x)
        rowInt += 1
    p = {filename : f}
with open('stress_data/' + filename + '/'+device+'.csv','rb') as ecg:
    reader = csv.reader(ecg)
    rowInt = 0
    flag = 'null'
    temp = []
    for row in reader:
        if rowInt != 0:
            colInt = 0
            for col in row:
                if colInt == 0:
                    if flag == 'null':
                        temp =[]
                        for key in p[filename]:
                            if (int(col) - int(p[filename][key][0])) <= 4 and (int(col) - int(p[filename][key][0])) >= 0:
                                num +=1
                                flag = key
                                temp.append(row)
                    else:
                        temp.append(row)
                        if (int(col) - int(p[filename][flag][1])) <= 4 and (int(col) - int(p[filename][flag][1])) >= 0:      
                            with open('stress_data/'+filename+'/'+device+'/'+device+'_'+flag+'.csv', 'wb') as newfile:
                                writer = csv.writer(newfile)
                                writer.writerows(temp)
                            flag = 'null'
                colInt += 1
        rowInt +=1

           
           
            
                          


import os
import csv
num =0
"""for filename in os.listdir('stress_data'):"""
filename = 'participant14'
device = 'neulog'
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
            time = int(row[2])
            print time
            if flag == 'null':
                temp =[]
                for key in p[filename]:
                    if (time >= int(p[filename][key][0])):
                        num +=1
                        flag = key
                        temp.append(row)
            else:
                temp.append(row)
                if (time >= int(p[filename][flag][1])):
                    with open('stress_data/'+filename+'/'+device+'/'+device+'_'+flag+'.csv', 'wb') as newfile:
                        writer = csv.writer(newfile)
                        writer.writerows(temp)
                        print p
                        print p[filename][flag]
                        del p[filename][flag]
                        flag = 'null'
        rowInt +=1

           
           
            
                          


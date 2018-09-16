function [subdur]= getRpeaks(subject1)

    load ECG_data.mat;
    baseecg=ECG;
    fs = 125 
    
    load cal_svm.mat;
    load cal_net.mat;
    load cal_thre.mat;
%     subject1 = transpose(subject)
%     subject1 = csvread('noise.csv');
    subject1 = transpose(subject1);

    [ecg1,predicts1] = clean_ecg(svm,net,threshold,subject1,fs, baseecg);  
    i1 = find(ecg1, 1, 'first');
    if i1 > 1
        ecg1(1:i1) = [];
    end

    subdur = pan_tompkin3(ecg1,fs,0);
end






    
    
    
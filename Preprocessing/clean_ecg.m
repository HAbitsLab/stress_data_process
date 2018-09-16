function [ecg,predicts]= clean_ecg(svmStruct,net,threshold,subject,fs,ECG)
%     figure(555);
%     plot(subject);
    subject=pandpass(subject,fs);
    ECG=pandpass(ECG,400);
    ecg2=normalize(ECG,subject,fs);
%     figure(666);
%     plot(ecg2);
    
    predicts= getPredict(svmStruct,net,threshold,ecg2,fs);
    
    %clean ecg
    windownum= length(predicts);
    ecg= ecg2(1:windownum*fs*0.6);
    predicts=predicts==1;
    for i=1:length(predicts)
        if predicts(i)==1
            ecg((i-1)*fs*0.6+1:i*fs*0.6)=0;
        end
    end
    
end

function [ecg_bp]= pandpass(ecg, fs)
    f1=15; f2=30; N = 3;
    Wn=[f1 f2]*2/fs; 
    [a,b] = butter(N,Wn);
    ecg_bp= filtfilt(a,b,ecg);
end

function [ecg_norm]= normalize(ECG,ecg,fs)

    base= findAmp(ECG, 400);
       
    newamp= findAmp(ecg, fs);
    
    ecg_norm= ecg*(base/newamp);

end

function [predicts]= getPredict(svmStruct,net,threshold,ecg,fs)

    dim=36;
    testnum= fix(length(ecg)/(.6*fs));
    peaks= getSVMpeak(ecg, fs, testnum, dim);
    svmdata= getSVMdata(peaks);
    predict1 = svmclassify(svmStruct,svmdata);
    predict1 = predict1';
    
    dim=36;
    nndata=getNNdata(ecg, fs, testnum, dim);
    nnthreshold=.5;
    predict2= net(nndata);
    predict2(predict2>=nnthreshold)=1;
    predict2(predict2<nnthreshold)=0;
    
    thredata=getThredata(peaks);
    thredata=thredata';
%     thredata.*10^7
%     threshold*10^7
    predict3 = thredata>threshold;
%     predict3 = predict3';
    
    predict0= predict2+predict1;
    predict0=(predict0==2);
%     predict0(predict0==2)=1;
    predict=predict0+predict3;
    predicts=(predict>0);

end

function [data]= getThredata(peaks)
    len= size(peaks,1);
    data=[];
    for i=1:len
        peak= peaks(i,:);
        peak=sort(peak);
        peak(peak==0)=[];
        b=max(peak);
        x= b;
%         newdata=[median(peak) max(peak)];
        newdata=[x ];
        data=[data; newdata];
    end
end

function [data]= getSVMdata(peaks)
    len= size(peaks,1);
    data=[];
    for i=1:len
        peak= peaks(i,:);
        peak=sort(peak);
        peak(peak==0)=[];
        a=prctile(peak,10);
        b=prctile(peak,20);
        c=prctile(peak,30);
        d=prctile(peak,80);
        
        e=prctile(peak,50);
        f=prctile(peak,60);
        x= max(peak);
        newdata=[a b c d];
        newdata=[ e f x];
        data=[data; newdata];
    end
end

function [data]= getSVMpeak(ecg, fs, windownum, dim)
    data=[];
    
    tol= windownum*fs*.6;
    ecg= ecg(1:tol);
    windowsize= 0.6*fs;
    
    for sec= 0:windownum-1
        addone= zeros(1,dim);
        ecgsub= ecg(sec*windowsize+1:(sec+1)*windowsize);
        ecgsub=abs(ecgsub);
        peaks1= findpeaks(ecgsub);
%         peaks2= findpeaks(-ecgsub);
%         peaks= [peaks1; peaks2];
        peaks=peaks1;
        plen= length(peaks);
        addone(1:plen)=peaks;
        data=[data; addone];
        
    end

end

function [data]= getNNdata(ecg, fs, windownum, dim)
%     dim= 30;
    data=[];
    
    f1=15; % 0.6Hz cuttoff low frequency to get rid of baseline wander 
    f2=30; % 200Hz cuttoff frequency to discard high frequency noise 
    Wn=[f1 f2]*2/fs; % cutt off based on fs
    N = 3; % order of 3 less processing
    [a,b] = butter(N,Wn); %bandpass filtering
    
    ecg= filtfilt(a,b,ecg);
    
%     tol= windownum*fs*.6;
%     ecg= ecg(1:tol);
    windowsize= 0.6*fs;
    
    for sec= 0:windownum-1
        addone= zeros(1,dim);
        ecgsub= ecg(sec*windowsize+1:(sec+1)*windowsize);
        peaks1= findpeaks(ecgsub);
        peaks2= -findpeaks(-ecgsub);
        peaks= [peaks1; peaks2];
        plen= length(peaks);
        if(plen > 36);
            peaks = peaks(1:36);
            plen = 36;
        end
        addone(1:plen)=peaks;
        addone=sort(addone);
        data=[data; addone];
        
    end
    data=data';

end

function [amplitude]= findAmp(ecg, fs)
	winsize=1.5;
    ecglen= length(ecg);
    winnum= fix(ecglen/(fs*winsize));  % 1.5 sec window
    amplist= [];
    for w=1:winnum
        ecgsub= ecg((w-1)*fs*winsize+1:w*fs*winsize);
        peak= max(ecgsub);
        valley= min(ecgsub);
%         valley= -max(-ecgsub);
        amplist= [amplist peak];%-valley];
    end
    
    percentile=10;
    amplist=sort(amplist);
    amplitude= prctile(amplist, percentile);
    
end

        
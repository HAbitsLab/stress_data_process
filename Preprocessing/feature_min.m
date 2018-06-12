function [subdur1]= feature_min()

%% classifier

    load ECG_data.mat;
    baseecg=ECG;

%% participant

    fs= 250;
% svm= SVM(0,0);
% net= NN(0,0);
% threshold=Thresh(0,0);
    load cal_svm.mat;
    load cal_net.mat;
    load cal_thre.mat;
% feature=[];
% duration=[];
% num_min=[];
    subject1 = csvread('noise.csv');
    [ecg1,predicts1] = clean_ecg(svm,net,threshold,subject1,fs, baseecg);   
    subdur1= dur_clean(predicts1,ecg1,fs);
    subdur1(isnan(subdur1))=[];
end
% num_dur=[num_dur length(subdur1)];
% participant = 'participant22';
% savename='p22_min_feature.mat';
% savelabel='p22_min_label';
% for i=1:16
%     i=i
%     num_dur=[];
%     subdur=[];
%     % get file path. order: prep speech arithmetic ice cry social eat sing
%         % game stroop Rest1-6
%     if i==5
%         num=3;
%         num_min=[num_min num];
%         filepath1=['/Users/zhanglida/Documents/MATLAB/stress2/stress_data/',participant,'/51.csv'];
%         subject1= csvread(filepath1); 
%         subject1=subject1(:,2);
%         [ecg1,predicts1] = clean_ecg(svm,net,threshold,subject1,fs, baseecg);   
%         subdur1= dur_clean(predicts1,ecg1,fs);
%         subdur1(isnan(subdur1))=[];
%         num_dur=[num_dur length(subdur1)];
%         filepath2=['/Users/zhanglida/Documents/MATLAB/stress2/stress_data/',participant,'/52.csv'];
%         subject2= csvread(filepath2);  
%         subject2=subject2(:,2);
%         [ecg2,predicts2] = clean_ecg(svm,net,threshold,subject2,fs, baseecg);   
%         subdur2= dur_clean(predicts2,ecg2,fs);
%         subdur2(isnan(subdur2))=[];
%         num_dur=[num_dur length(subdur2)];
%         filepath3=['/Users/zhanglida/Documents/MATLAB/stress2/stress_data/',participant,'/53.csv'];
%         subject3= csvread(filepath3);   
%         subject3=subject3(:,2);
%         [ecg3,predicts3] = clean_ecg(svm,net,threshold,subject3,fs, baseecg);   
%         subdur3= dur_clean(predicts3,ecg3,fs);
%         subdur3(isnan(subdur3))=[];
%         num_dur=[num_dur length(subdur3)];
%         subdur=[subdur1 subdur2 subdur3];
%         duration=[duration subdur];
%         
%     else % except infant cry 
%         if i<=10
%             filepath=['/Users/zhanglida/Documents/MATLAB/stress2/stress_data/',participant,'/',num2str(i),'.csv']            
%         else % rest
%             filepath=['/Users/zhanglida/Documents/MATLAB/stress2/stress_data/',participant,'/ecg_rest',num2str(i-10),'.csv']           
%         end
%         subject= csvread(filepath);
%         subject=subject(:,2);
%         
%         num=ceil((length(subject)-30*fs)/(fs*30)); %overlap
%         num_min=[num_min num];
%         for m=1:num
%             if m==num
%                 subecg=subject((m-1)*30*fs+1:end);
%             else
%                 subecg=subject((m-1)*30*fs+1:(m-1)*30*fs+60*fs);
%             end
% %             subecg=subject((m-1)*60*fs+1:m*60*fs);
%             [ecg_clean,predicts] = clean_ecg(svm,net,threshold,subecg,fs, baseecg);
%             subdur= dur_clean(predicts,ecg_clean,fs);
% 
%             num_dur=[num_dur length(subdur)];
%             duration=[duration subdur];
%             
%         end
%     end
% 
%     lastdur=0;
%     for ii=1:length(num_dur)
%         ii
%         ddsub=duration(lastdur+1:lastdur+num_dur(ii));
%         lastdur=lastdur+num_dur(ii);
%         subdur=ddsub;
%         diff=successiveDiff(subdur);
%         nn20=diff(diff>20);
%         nn20(isnan(nn20))=[];
%         nn50=diff(diff>50);
%         nn50(isnan(nn50))=[];
%         RMSSD=mean(diff.*diff)^.5;
%         SDSD=std(diff);
%         pnn20=length(nn20)/length(diff);
%         pnn50=length(nn50)/length(diff);
%         
%         subdur(isnan(subdur))=[];
%         
%         meanRR=mean(subdur);
%         medianRR=median(subdur);
%         variance=var(subdur);
%         quartiled=iqr(subdur); %Interquartile range
%         %quartiled=prctile(ddsub,75)-prctile(ddsub,25);
%         maxRR=max(subdur);
%         minRR=min(subdur);
%         range=maxRR-minRR;
%         percentile80=prctile(subdur,80);
%         percentile20=prctile(subdur,20);
%         HF=0;
%         LF=0;
% %         if length(subdur)>5
%         [HF, LF]=freqdomain(subdur,fs);
% %         end
%    
%         feature_sub=[meanRR medianRR variance quartiled range maxRR minRR percentile80 percentile20 HF LF LF/HF RMSSD SDSD pnn20 pnn50];    
%         feature=[feature; feature_sub];
%         
%     end
%     hr=60./(subdur/1000);
%     figure(100+i);
%     plot(hr);
%     
% end
% num_min
% featureshow=feature';
% save(savename, 'feature');
% save(savelabel, 'num_min');
% 
% end
% 
function[diff]=successiveDiff(duration)
    diff=[];
    len=length(duration);
    i=1;
    while i<len && isnan(duration(i))
            i=i+1;
    end
    while i<len
        if isnan(duration(i+1))
            i=i+1;
            while i<=len && isnan(duration(i))
                i=i+1;
            end
        else
            diff=[diff abs(duration(i)-duration(i+1))];
            i=i+1;
        end       
    end
end

function duration= dur_clean(predicts,ecg,fs)
    
    %get R-peaks
    qrs_raw= pan_tompkin3(ecg,fs,0);    
%     a=pan_tompkin1(ecg,fs,1);

    duration=[];
    
    len=length(qrs_raw);
    for i=1:len-1
        curpos= qrs_raw(i);
        curwin= ceil(curpos/(fs*0.6));
        nextpos= qrs_raw(i+1);
        nextwin= ceil(nextpos/(fs*0.6));
        if sum(predicts(curwin:nextwin))==0% && mod(nextpos,fs*0.5)~=0 && mod(curpos,fs*0.5)~=0
            duration=[duration nextpos-curpos];
        end
    end        
    
    duration=duration*1000/fs;
    len1=length(duration);
    
    isvalid= CBD4(duration, ones(1,length(duration)),fs); % heart rate cal: keep position. Do not need to keep position here.
    duration= duration.*isvalid;
    duration(duration==0)=NaN;
    
end

function []=hr_plot(dur, xx,test)
    figure;
    before=0;
    for i=1:test
        dursub=dur(xx(i)+1:xx(i+1));
        num=fix(length(xx)/5);
        hr=[];
        for n=1:num
            s=sum(dursub((n-1)*5+1:n*5));
            hr=[hr s/5];
        end
        hr=60./(hr./250);
        plot([before+1:before+num],hr);
        hold on;
        before=before+num;
    end
end

function [HF, LF]=freqdomain(duration, fs)

    duration1=interp(duration,fs);
    L = length(duration1);
    f = fs*(0:(L/2))/L;
    Y = fft(duration1);
    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);


    ct1=0;
    for l1=1:length(f)
        if(f(1,l1)>=.15&&f(1,l1)<.4)
%         if(f(1,l1)>=.04&&f(1,l1)<.15)
            ct1=ct1+1;
            Y1(1,ct1)=f(1,l1);
            Y1(2,ct1)=P1(1,l1);
        end
    end
    T1=Y1(2,:);%.*0.0104;
    HF=sum(T1);
    
    ct2=0;
    for l2=1:length(f)
        if(f(1,l2)>=.04&&f(1,l2)<.15)
            ct2=ct2+1;
            Y2(1,ct2)=f(1,l2);
            Y2(2,ct2)=P1(1,l2);
        end
    end
    T2=Y2(2,:);%.*0.0104;
    LF=sum(T2);

end 


    
    
    
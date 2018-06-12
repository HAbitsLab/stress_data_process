function [ isvalid ] = CBD4( durations, qrs_valid,fs )
durations=durations./1000;
if mean(durations>10)
    durations=durations./fs;
end

dur_valid= durations(qrs_valid==1);

IQ= prctile(dur_valid,75)- prctile(dur_valid,25);

% sortperiod = sort(dur_valid);
% quartile=ceil(length(dur_valid)/4);
% IQ= sortperiod(quartile*3)-sortperiod(quartile);

QD= IQ*0.5;
% QD=sortperiod(quartile*3)-(sortperiod(quartile)/2);
MED= 3.32*QD;
% median= sortperiod(ceil(length(dur_valid)/2));
medians= median(dur_valid);
MAD=(medians-2.9*QD)/3;
CBD= (MAD + MED)/2;
RRk=0;

isvalid=qrs_valid;
startpos=1;
while startpos< length(durations)-1.5
    if qrs_valid(startpos)==0
        startpos= startpos+1;
    end
    if 0.3<durations(startpos) && durations(startpos)<1.5
        if abs(durations(startpos)-durations(startpos+1))<CBD %&& abs(durations(startpos)-durations(startpos+2))<CBD
            RRk= durations(startpos);
            break;
        else
            isvalid(startpos)=0;
            startpos= startpos+1;
        end
    else
        isvalid(startpos)=0;
        startpos= startpos+1;
    end
end

for i=startpos+1:length(durations)
    if qrs_valid(i)==0
        continue;
    end
    x = durations(i);
    if 0.3<durations(i) && durations(i)<1.5
        if isvalid(i-1)==1
            if abs(durations(i)-durations(i-1))<=CBD
                isvalid(i)=1;
                RRk=durations(i);
            else
             
                isvalid(i)=0;
            end
        else
            
            if abs(durations(i)-RRk)<=1.8*CBD
                isvalid(i)=1;
                RRk=durations(i);
            else
                
                isvalid(i)=0;
            end
        end
    else
        
        isvalid(i)=0;
    end

% if abs(durations(end)-RRk)>CBD
%     isvalid(i)=0;
% end

% period =sort(period);

end




# stress_data_process

Stress_Preprocessing and stress_data_process essentially accomplish the same thing except stress_data_process uses Lidas original
SVM code while Stress_Prespocessing uses begums ne SVM classify


Important functions are in the Preporcessing folder and mainSegments.py contains the function that will clean and get the rpeaks from the ECG data.  It also will calculate the features for each day of ECG data and create a features.csv file in each of the participants data file.

# -*- coding: utf-8 -*-
"""WPD_Classifying_heartbeat_features_WPD .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UXcISKKVOy1Q5JFNCJwTiDeWR9jgWkeA

Details and Resources of the project in the doc:                                
https://docs.google.com/document/d/1F-KYQ5nRnDAUVDUrEbTFYGn7TEVsT8EByuM9xJLT4gA/edit
"""

# Commented out IPython magic to ensure Python compatibility.
import warnings                        # To ignore any warnings
warnings.filterwarnings("ignore")
# %matplotlib inline
# %pylab inline
import os
import pandas as pd
import librosa
import librosa.display
import glob 
import matplotlib.pyplot as plt
# %config InlineBackend.figure_format = 'retina'

import seaborn as sns; sns.set()
import scipy.io as sio
# descriptive statistics
import scipy as sp
import scipy.stats as stats
import pywt

from google.colab import drive
drive.mount("/content/drive")

INPUT_DIR = '/content/drive/MyDrive/AI ML Things/University of Turku Research Internship'
'''
set_a_path=base_path+'/set_a'
set_a_metadata_path=base_path+'/set_a.csv'
set_b_path=base_path+'/set_b'
set_b_metadata_path=base_path+'/set_b.csv'
set_a_metadata = pd.read_csv(set_a_metadata_path)
'''
dataset_path = INPUT_DIR+'/set_a'
metadata = pd.read_csv(INPUT_DIR+'/set_a.csv')

SAMPLE_RATE = 16000
# seconds
MAX_SOUND_CLIP_DURATION=12

"""#Explorer data"""

set_a=pd.read_csv(INPUT_DIR+"/set_a.csv")
set_a.head()

set_a_timing=pd.read_csv(INPUT_DIR+"/set_a_timing.csv")
set_a_timing.head()

set_b=pd.read_csv(INPUT_DIR+"/set_b.csv")
set_b.head()

#merging both set-a and set-b
frames = [set_a, set_b]
train_ab=pd.concat(frames)
train_ab.describe()

#checking for duplicates
nb_classes=train_ab.label.unique()

print("Number of training examples=", train_ab.shape[0], "  Number of classes=", len(train_ab.label.unique()))
print (nb_classes)

"""Note: 'nan' indicate unclassified and unlabel test files"""

# visualize data distribution by category
category_group = train_ab.groupby(['label','dataset']).count()
plot = category_group.unstack().reindex(category_group.unstack().sum(axis=1).sort_values().index)\
          .plot(kind='bar', stacked=True, title="Number of Audio Samples per Category", figsize=(16,5))
plot.set_xlabel("Category")
plot.set_ylabel("Samples Count");

print('Min samples per category = ', min(train_ab.label.value_counts()))
print('Max samples per category = ', max(train_ab.label.value_counts()))

print('Minimum samples per category = ', min(train_ab.label.value_counts()))
print('Maximum samples per category = ', max(train_ab.label.value_counts()))

"""##Exploring each category individually"""





"""#Extracting Features of Data in Audio Domain

##Sound Feature: MFCCs
"""

# Checking an example generate mfccs from a audio file
example_file=INPUT_DIR+"/set_a/normal__201106111136.wav"
#y, sr = librosa.load(sample_file, offset=7, duration=7)
y, sr = librosa.load(example_file)
y

y.shape

"""#Loading Data"""

print("Number of training examples=", train_ab.shape[0], "  Number of classes=", len(train_ab.label.unique()))

# get audio data with a fix padding may also chop off some file
def load_file_data (folder,file_names, duration=12, sr=16000):
    input_length=sr*duration
    # function to load files and extract features
    # file_names = glob.glob(os.path.join(folder, '*.wav'))
    data = []
    for file_name in file_names:
        try:
            sound_file=folder+file_name
            print ("load file ",sound_file)
            # use kaiser_fast technique for faster extraction
            X, sr = librosa.load( sound_file, sr=sr, duration=duration,res_type='kaiser_fast') 
            dur = librosa.get_duration(y=X, sr=sr)
            # pad audio file same duration
            if (round(dur) < duration):
                print ("fixing audio lenght :", file_name)
                y = librosa.util.fix_length(X, input_length)                
            #normalized raw audio 
            # y = audio_norm(y)            
            # extract normalized mfcc feature from data
                        
        except Exception as e:
            print("Error encountered while parsing file: ", file)        
        
        data.append(y)
    return data

# load dataset-a, keep them separate for testing purpose
import os, fnmatch

A_folder=INPUT_DIR+'/set_a/'
# set-a
A_artifact_files = fnmatch.filter(os.listdir(INPUT_DIR+'/set_a'), 'artifact*.wav')
A_artifact_sounds = load_file_data(folder=A_folder,file_names=A_artifact_files, duration=MAX_SOUND_CLIP_DURATION)
A_artifact_labels = [0 for items in A_artifact_files]

arr=np.asarray(A_artifact_sounds)

arr.shape

arr

arr=np.transpose(arr)

arr.shape

db1 = pywt.Wavelet('db1')
temp_list = [] #for Class Labels

###############################
"""Extract The Coeeficients"""
Length = 1024;    # Length of signal
Nofsignal=400; #Number of Signal for each Class
numrows = len(arr)   
numrows =83     #Number of features extracted from Wavelet Packet Decomposition 
numcols = len(arr[0]) 

Extracted_Features=np.ndarray(shape=(3*numcols,numrows), dtype=float, order='F')

for i in range(numcols):
    wp= pywt.WaveletPacket(arr[:,i], db1, mode='symmetric', maxlevel=6)
    Extracted_Features[i,0]=sp.mean(abs(wp['a'].data))
    Extracted_Features[i,1]=sp.mean(abs(wp['aa'].data))
    Extracted_Features[i,2]=sp.mean(abs(wp['aaa'].data))
    Extracted_Features[i,3]=sp.mean(abs(wp['aaaa'].data))
    Extracted_Features[i,4]=sp.mean(abs(wp['aaaaa'].data))
    Extracted_Features[i,5]=sp.mean(abs(wp['aaaaaa'].data))
    Extracted_Features[i,6]=sp.mean(abs(wp['d'].data))
    Extracted_Features[i,7]=sp.mean(abs(wp['dd'].data))
    Extracted_Features[i,8]=sp.mean(abs(wp['ddd'].data))
    Extracted_Features[i,9]=sp.mean(abs(wp['dddd'].data))
    Extracted_Features[i,10]=sp.mean(abs(wp['ddddd'].data))
    Extracted_Features[i,11]=sp.mean(abs(wp['dddddd'].data))

    Extracted_Features[i,12]=sp.std(wp['a'].data)
    Extracted_Features[i,13]=sp.std(wp['aa'].data)
    Extracted_Features[i,14]=sp.std(wp['aaa'].data)
    Extracted_Features[i,15]=sp.std(wp['aaaa'].data)
    Extracted_Features[i,16]=sp.std(wp['aaaaa'].data)
    Extracted_Features[i,17]=sp.std(wp['aaaaaa'].data)
    Extracted_Features[i,18]=sp.std(wp['d'].data)
    Extracted_Features[i,19]=sp.std(wp['dd'].data)
    Extracted_Features[i,20]=sp.std(wp['ddd'].data)
    Extracted_Features[i,21]=sp.std(wp['dddd'].data)
    Extracted_Features[i,22]=sp.std(wp['ddddd'].data)
    Extracted_Features[i,23]=sp.std(wp['dddddd'].data)

    Extracted_Features[i,24]=sp.median(wp['a'].data)
    Extracted_Features[i,25]=sp.median(wp['aa'].data)
    Extracted_Features[i,26]=sp.median(wp['aaa'].data)
    Extracted_Features[i,27]=sp.median(wp['aaaa'].data)
    Extracted_Features[i,28]=sp.median(wp['aaaaa'].data)
    Extracted_Features[i,29]=sp.median(wp['aaaaaa'].data)
    Extracted_Features[i,30]=sp.median(wp['d'].data)
    Extracted_Features[i,31]=sp.median(wp['dd'].data)
    Extracted_Features[i,32]=sp.median(wp['ddd'].data)
    Extracted_Features[i,33]=sp.median(wp['dddd'].data)
    Extracted_Features[i,34]=sp.median(wp['ddddd'].data)
    Extracted_Features[i,35]=sp.median(wp['dddddd'].data)
    
    Extracted_Features[i,36]=stats.skew(wp['a'].data)
    Extracted_Features[i,37]=stats.skew(wp['aa'].data)
    Extracted_Features[i,38]=stats.skew(wp['aaa'].data)
    Extracted_Features[i,39]=stats.skew(wp['aaaa'].data)
    Extracted_Features[i,40]=stats.skew(wp['aaaaa'].data)
    Extracted_Features[i,41]=stats.skew(wp['aaaaaa'].data)
    Extracted_Features[i,42]=stats.skew(wp['d'].data)
    Extracted_Features[i,43]=stats.skew(wp['dd'].data)
    Extracted_Features[i,44]=stats.skew(wp['ddd'].data)
    Extracted_Features[i,45]=stats.skew(wp['dddd'].data)
    Extracted_Features[i,46]=stats.skew(wp['ddddd'].data)
    Extracted_Features[i,47]=stats.skew(wp['dddddd'].data)
    
    Extracted_Features[i,48]=stats.kurtosis(wp['a'].data)
    Extracted_Features[i,49]=stats.kurtosis(wp['aa'].data)
    Extracted_Features[i,50]=stats.kurtosis(wp['aaa'].data)
    Extracted_Features[i,51]=stats.kurtosis(wp['aaaa'].data)
    Extracted_Features[i,52]=stats.kurtosis(wp['aaaaa'].data)
    Extracted_Features[i,53]=stats.kurtosis(wp['aaaaaa'].data)
    Extracted_Features[i,54]=stats.kurtosis(wp['d'].data)
    Extracted_Features[i,55]=stats.kurtosis(wp['dd'].data)
    Extracted_Features[i,56]=stats.kurtosis(wp['ddd'].data)
    Extracted_Features[i,57]=stats.kurtosis(wp['dddd'].data)
    Extracted_Features[i,58]=stats.kurtosis(wp['ddddd'].data)
    Extracted_Features[i,59]=stats.kurtosis(wp['dddddd'].data)
    
    Extracted_Features[i,60]=np.sqrt(np.mean(wp['a'].data**2))   #RMS Value
    Extracted_Features[i,61]=np.sqrt(np.mean(wp['aa'].data**2))
    Extracted_Features[i,62]=np.sqrt(np.mean(wp['aaa'].data**2))
    Extracted_Features[i,63]=np.sqrt(np.mean(wp['aaaa'].data**2))
    Extracted_Features[i,64]=np.sqrt(np.mean(wp['aaaaa'].data**2))
    Extracted_Features[i,65]=np.sqrt(np.mean(wp['aaaaaa'].data**2))
    Extracted_Features[i,66]=np.sqrt(np.mean(wp['d'].data**2))
    Extracted_Features[i,67]=np.sqrt(np.mean(wp['dd'].data**2))
    Extracted_Features[i,68]=np.sqrt(np.mean(wp['ddd'].data**2))
    Extracted_Features[i,69]=np.sqrt(np.mean(wp['dddd'].data**2))
    Extracted_Features[i,70]=np.sqrt(np.mean(wp['ddddd'].data**2))
    Extracted_Features[i,71]=np.sqrt(np.mean(wp['dddddd'].data**2))
    
    Extracted_Features[i,72]=sp.mean(abs(wp['a'].data))/sp.mean(abs(wp['aa'].data))
    Extracted_Features[i,73]=sp.mean(abs(wp['aa'].data))/sp.mean(abs(wp['aaa'].data))
    Extracted_Features[i,74]=sp.mean(abs(wp['aaa'].data))/sp.mean(abs(wp['aaaa'].data))
    Extracted_Features[i,75]=sp.mean(abs(wp['aaaa'].data))/sp.mean(abs(wp['aaaaa'].data))
    Extracted_Features[i,76]=sp.mean(abs(wp['aaaaa'].data))/sp.mean(abs(wp['aaaaaa'].data))
    Extracted_Features[i,77]=sp.mean(abs(wp['aaaaaa'].data))/sp.mean(abs(wp['d'].data))
    Extracted_Features[i,78]=sp.mean(abs(wp['d'].data))/sp.mean(abs(wp['dd'].data))
    Extracted_Features[i,79]=sp.mean(abs(wp['dd'].data))/sp.mean(abs(wp['ddd'].data))
    Extracted_Features[i,80]=sp.mean(abs(wp['ddd'].data))/sp.mean(abs(wp['dddd'].data))
    Extracted_Features[i,81]=sp.mean(abs(wp['dddd'].data))/sp.mean(abs(wp['ddddd'].data))
    Extracted_Features[i,82]=sp.mean(abs(wp['ddddd'].data))/sp.mean(abs(wp['dddddd'].data))
    
    temp_list.append("A_artifact_sounds")

Extracted_Features.shape


















































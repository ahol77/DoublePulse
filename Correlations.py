# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 23:44:26 2019

@author: aholm
"""

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

#Calibration factor for Center Pixel
Calibration = 0.0475 #ev/pixel

#Import concatenated data
Data = pd.read_pickle('./EditedData/EditedAllData.pkl')

#Choose param to sort the specs by
#This will determine what parameters the data is grouped by
x1="Seed Amplitude"
x2="Seed Energy"
x3="SASE Amplitude"
x4="SASE Energy"
Sort = x2

Data=Data.sort_values(by=[Sort])

#Import parameters of each spec
SpecNum = Data['Spec Number'].values.tolist()
ShotSpec = Data['Shot Spec_x'].values.tolist()

SeedDom = Data['Seed Domain'].values.tolist()
SeedGauss = Data['Seed Gaussian Fit'].values.tolist()

SASEDom = Data['SASE Domain'].values.tolist()
SASEGauss = Data['SASE Gaussian Fit'].values.tolist()

SeedAmp = Data['Seed Amplitude'].values.tolist()
SeedWave = np.array(Data['Seed Energy'].values.tolist()) * Calibration
SeedSigma = Data['Seed Sigma'].values.tolist()
SeedLinear = Data['Seed Linear'].values.tolist()
SeedConstant = Data['Seed Constant'].values.tolist()

SASEAmp = Data['SASE Amplitude'].values.tolist()
SASEWave = np.array(Data['SASE Energy'].values.tolist()) * Calibration
SASESigma = Data['SASE Sigma'].values.tolist()
SASELinear = Data['SASE Linear'].values.tolist()
SASEConstant = Data['SASE Constant'].values.tolist()

SeedArea = Data['Seed Area'].values.tolist()
SASEArea = Data['SASE Area'].values.tolist()

#Define correlation function with input of two parameters
def corr(Param1,Param2):
    Param1Average = np.mean(Param1)
    Param2Average = np.mean(Param2)
    n = len(Param1)
    numm = 0
    denom1 = 0
    denom2 = 0
    for i in range(n):
        numm += (Param1[i]-Param1Average)*(Param2[i]-Param2Average)
        denom1 += (Param1[i]-Param1Average)**2
        denom2 += (Param2[i]-Param2Average)**2
    corr = numm / np.sqrt(denom1 * denom2)
    return corr

#Create way to group data in order to overcome noise
#May need to remove some datapoints to allow good number of groups
#Remove first number of specs
first=0
#Remove last number of specs
last=-46
#Number of specs in each bin
group=205
#Group the params
GroupedSeedAmp=np.reshape(SeedAmp[first:last],[-1,group])
GroupedSeedWave=np.reshape(SeedWave[first:last],[-1,group])
GroupedSASEAmp=np.reshape(SASEAmp[first:last],[-1,group])
GroupedSASEWave=np.reshape(SASEWave[first:last],[-1,group])

#Take average of each group
SeedWaveAvg=np.mean(GroupedSeedWave, axis=1)[0:-1]
SeedAmpAvg=np.mean(GroupedSeedAmp, axis=1)[0:-1]
SASEWaveAvg=np.mean(GroupedSASEWave, axis=1)[0:-1]
SASEAmpAvg=np.mean(GroupedSASEAmp, axis=1)[0:-1]

#Automatically label and select indpendent variable depending on sort
if Sort == x1:
    avgx = SeedAmpAvg
    normalx = SeedAmp
elif Sort == x2:
    avgx = SeedWaveAvg
    normalx = SeedWave
elif Sort == x3:
    avgx = SASEAmpAvg
    normalx = SASEAmp
elif Sort == x4:
    avgx = SASEWaveAvg
    normalx = SASEWave

#Plot histogram of selected bin
plt.figure()
plt.xlabel(Sort)
plt.ylabel('Counts')
plt.hist(normalx,100)

#Compare seed and SASE params
plt.figure()
plt.subplot(2,2,1)
plt.xlabel(Sort)
plt.ylabel("Seed Amplitude")
plt.plot(normalx,SeedAmp,'.',markersize=1)
corr1=corr(normalx,SeedAmp)
plt.text(np.min(normalx),np.max(SeedAmp),"Correlation: "+str(corr1), verticalalignment='top',fontsize=14)

plt.subplot(2,2,2)
plt.xlabel(Sort)
plt.ylabel("Seed Energy")
plt.plot(normalx,SeedWave,'.',markersize=1)
corr2=corr(normalx,SeedWave)
plt.text(np.min(normalx),np.max(SeedWave),"Correlation: "+str(corr2), verticalalignment='top',fontsize=14)

plt.subplot(2,2,3)
plt.xlabel(Sort)
plt.ylabel("SASE Amplitude")
plt.plot(normalx,SASEAmp,'.',markersize=1)
corr3=corr(normalx,SASEAmp)
plt.text(np.min(normalx),np.max(SASEAmp),"Correlation: "+str(corr3), verticalalignment='top',fontsize=14)

plt.subplot(2,2,4)
plt.xlabel(Sort)
plt.ylabel("SASE Energy")
plt.plot(normalx,SASEWave,'.',markersize=1)
corr4=corr(normalx,SASEWave)
plt.text(np.min(normalx),np.max(SASEWave),"Correlation: "+str(corr4), verticalalignment='top',fontsize=14)

#Compare seed and SASE avg params
plt.figure()
plt.subplot(2,2,1)
plt.xlabel(Sort)
plt.ylabel("Seed Amplitude")
plt.plot(avgx,SeedAmpAvg,'.')
corr1=corr(avgx,SeedAmpAvg)
plt.text(np.min(avgx),np.max(SeedAmpAvg),"Correlation: "+str(corr1), verticalalignment='top',fontsize=14)

plt.subplot(2,2,2)
plt.xlabel(Sort)
plt.ylabel("Seed Energy")
plt.plot(avgx,SeedWaveAvg,'.')
corr2=corr(avgx,SeedWaveAvg)
plt.text(np.min(avgx),np.max(SeedWaveAvg),"Correlation: "+str(corr2), verticalalignment='top',fontsize=14)

plt.subplot(2,2,3)
plt.xlabel(Sort)
plt.ylabel("SASE Amplitude")
plt.plot(avgx,SASEAmpAvg,'.')
corr3=corr(avgx,SASEAmpAvg)
plt.text(np.min(avgx),np.max(SASEAmpAvg),"Correlation: "+str(corr3), verticalalignment='top',fontsize=14)

plt.subplot(2,2,4)
plt.xlabel(Sort)
plt.ylabel("SASE Energy")
plt.plot(avgx,SASEWaveAvg,'.')
corr4=corr(avgx,SASEWaveAvg)
plt.text(np.min(avgx),np.max(SASEWaveAvg),"Correlation: "+str(corr4), verticalalignment='top',fontsize=14)
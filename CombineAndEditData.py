# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 18:10:18 2019

@author: aholm
"""

import numpy as np
import pandas as pd
import os

if not os.path.exists('./EditedData'):
    os.makedirs('./EditedData')

#Calibration factor for Center Pixel
Calibration = 0.0475 #ev/pixel

#Initalize array to iterate through all datasets
dataset = np.arange(1,12)+ 2770
Data = pd.read_pickle('./GoodData/Data2770.pkl')
#Concatenate all of the datasets into one large dataset containing all experiments
for i in range(len(dataset)):
    data=dataset[i]
    NewData = pd.read_pickle('./GoodData/Data'+str(data)+'.pkl')
    Data= pd.concat([Data,NewData])

Data.to_pickle('./EditedData/GoodData.pkl')

#Initalize array to iterate through all datasets
baddataset = np.arange(1,12)+ 2770
BadData = pd.read_pickle('./BadSeedData/BadSeedData2770.pkl')
#Concatenate all of the datasets into one large dataset containing all experiments
for i in range(len(baddataset)):
    baddata=baddataset[i]
    BadNewData = pd.read_pickle('./BadSeedData/BadSeedData'+str(baddata)+'.pkl')
    BadData= pd.concat([BadData,BadNewData])

BadData.to_pickle('./EditedData/BadData.pkl')

#Remove all SASE wavelengths that are not within 300-700 pixels
SASEWave = Data['SASE Energy'].values.tolist()
droplist=[]
for i in range(len(SASEWave)):
    if 300>=SASEWave[i] or 700<=SASEWave[i]:
        droplist.append(i)
Data=Data.drop(Data.index[droplist])

#Remove all SASE Amplitudes that are below 20000
SASEAmp = Data['SASE Amplitude'].values.tolist()
droplist=[]
for i in range(len(SASEAmp)):
    if 20000>=SASEAmp[i]:
        droplist.append(i)
Data=Data.drop(Data.index[droplist])

#Load in all arrays
SpecNum = Data['Spec Number'].values.tolist()
ShotSpec = Data['Shot Spec_x'].values.tolist()

SeedDom = Data['Seed Domain'].values.tolist()
SeedGauss = Data['Seed Gaussian Fit'].values.tolist()

SASEDom = Data['SASE Domain'].values.tolist()
SASEGauss = Data['SASE Gaussian Fit'].values.tolist()

SeedAmp = Data['Seed Amplitude'].values.tolist()
SeedWave = Data['Seed Energy'].values.tolist()
SeedSigma = Data['Seed Sigma'].values.tolist()
SeedLinear = Data['Seed Linear'].values.tolist()
SeedConstant = Data['Seed Constant'].values.tolist()

SASEAmp = Data['SASE Amplitude'].values.tolist()
SASEWave = Data['SASE Energy'].values.tolist()
SASESigma = Data['SASE Sigma'].values.tolist()
SASELinear = Data['SASE Linear'].values.tolist()
SASEConstant = Data['SASE Constant'].values.tolist()

#Def a way to calculate area of the gaussian
def Area(Amp,Wave,Sigma,Linear,Constant,Domain):
    up=Domain[-1]
    low=Domain[0]
    area = (Amp*np.sqrt(2*np.pi)*Sigma*np.exp(-(up-Wave)**2/(2*Sigma**2)) -
            Amp*np.sqrt(2*np.pi)*Sigma*np.exp(-(low-Wave)**2/(2*Sigma**2)) +
            0.5*Linear*(up**2-low**2) + Constant*(up-low))
    return area

SeedArea=[]
SASEArea=[]
#Append areas to an array
for i in range(len(SeedAmp)):
    SeedArea.append(Area(SeedAmp[i],SeedWave[i],SeedSigma[i],SeedLinear[i],SeedConstant[i],SeedDom[i]))
    SASEArea.append(Area(SASEAmp[i],SASEWave[i],SASESigma[i],SASELinear[i],SASEConstant[i],SASEDom[i]))

#Append to the main dataset to use later
Data['Seed Area'] = np.array(SeedArea)
Data['SASE Area'] = np.array(SASEArea)

Data.to_pickle('./EditedData/EditedAllData.pkl')

#Split data by a wavelength limit
Data=Data.sort_values(by=['SASE Energy'])
cond=0
split=0
SASEWave = Data['SASE Energy'].values.tolist()
while cond == 0:
    if SASEWave[split] <= 475:
        split+=1
    else:
        cond = 1

First=Data.iloc[:split]
Last=Data.iloc[split:]

First.to_pickle('./EditedData/FirstSASEData.pkl')
Last.to_pickle('./EditedData/LastSASEData.pkl')

#Split data by a wavelength limit
Data=Data.sort_values(by=['Seed Energy'])
cond=0
split=0
SeedWave = np.array(Data['Seed Energy'].values.tolist()) * Calibration
while cond == 0:
    if SeedWave[split] <= 59.92:
        split+=1
    else:
        cond = 1

First=Data.iloc[:split]
Last=Data.iloc[split:]

First.to_pickle('./EditedData/FirstSeedData.pkl')
Last.to_pickle('./EditedData/LastSeedData.pkl')
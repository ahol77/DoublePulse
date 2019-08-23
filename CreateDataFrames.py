# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:24:09 2019

@author: aholm
"""

import numpy as np
import pandas as pd
import os
from LoadData import Load
from FitSeed import FitSeed
from FitSase import FitSASE

#Create directories to store files if they currently do not exist
if not os.path.exists('./BadSeedData'):
    os.makedirs('./BadSeedData')

if not os.path.exists('./GoodData'):
    os.makedirs('./GoodData')

#Create list to iterate over of all sync datasets
dataset = np.arange(0,12)+ 2770

for i in range(len(dataset)):
    #Select dataset number
    data = dataset[i]
    #Load in specs
    specs = Load(data)
    #Select good seeded regions
    Data = FitSeed(data,specs)
    #Select good SASE regions
    Data = FitSASE(data)
    #Load in datasets
    SeedData = pd.read_pickle('./GoodData/SeedData'+str(data)+'.pkl')
    PSASEData = pd.read_pickle('./GoodData/SASEData'+str(data)+'.pkl')
    #Combine datasets into one nice set for each specific number
    CombinedData = pd.merge(SeedData,PSASEData, on='Spec Number')
    CombinedData = CombinedData.sort_values(by=['Seed Amplitude'])
    CombinedData = CombinedData.drop(columns=['Shot Spec_y'])
    CombinedData.to_pickle('./GoodData/Data'+str(data)+'.pkl')
    os.remove('./GoodData/SeedData'+str(data)+'.pkl')
    os.remove('./GoodData/SASEData'+str(data)+'.pkl')
    print("Dataset "+str(data)+" Complete")
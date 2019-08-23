# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:02:22 2019

@author: aholm
"""

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

#Calibration factor for Center Pixel
Calibration = 0.0475 #ev/pixel

#Choose Dataset
data = './EditedData/BadData.pkl'
#Import concatenated data
Data = pd.read_pickle(data)

BadShotSpec = Data['Shot Spec'].values.tolist()

Badaverage = np.mean(BadShotSpec, axis=0)

#Choose Dataset
data = './EditedData/GoodData.pkl'
#Import concatenated data
Data = pd.read_pickle(data)

GoodShotSpec = Data['Shot Spec_x'].values.tolist()

Goodaverage = np.mean(GoodShotSpec, axis=0)

AllShots = GoodShotSpec + BadShotSpec
Allaverage = np.mean(AllShots, axis=0)

x = np.arange(0,2048) * Calibration

plt.figure()
plt.plot(x,Badaverage)
plt.plot(x,Goodaverage)
plt.plot(x,Allaverage)
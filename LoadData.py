# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:46:29 2019

@author: aholm
"""

import numpy as np
from scipy import io as sio

def Load(dataset):
    #Load specified dataset and retrieve the specs
    #More data could be retrieved if need to compare more information
    #Use Matlab to view the whole syncdata file
    Sync = sio.loadmat('./SyncData/syncdata'+str(dataset))['sync'][0,0]
    specs = np.transpose(Sync[6])
    return specs
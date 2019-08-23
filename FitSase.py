# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 10:54:49 2019

@author: aholm
"""

import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit as cf
import pandas as pd

def gaussian(x, amp, cen, sig, lin, lift):
    return amp * np.exp(-(x-cen)**2 / (2*sig**2)) + lin*x + lift

def FitSASE(dataset):
    #Fit the SASE region of the spectrum to a Gaussian
    #Import in the well fit seeded specs
    PositiveDataSet = pd.read_pickle('./GoodData/SeedData'+str(dataset)+'.pkl')
    
    Specs = PositiveDataSet['Shot Spec'].values.tolist()
    TrialNum = PositiveDataSet['Spec Number'].values.tolist()
    
    #Smooth out spec in order to reduce noise which is prevalent in the SASE
    smoothlist=[]
    for i in range(len(Specs)):
        #savgol process keeps domain intact
        #This number is the number of points to bin together
        average_number = 151
        smooth = savgol_filter(Specs[i],average_number,1)
        smoothlist.append(smooth)
    smoothlist=np.array(smoothlist)
    
    #Initalize lists to populate with fits
    newdomainlist=[]
    valueslist=[]
    fitlist=[]
    r2list=[]
    for i in range(len(smoothlist)):
        #Set bounds to check for maximum to begin fitting process
        lower=100
        upper=1000
        domain = np.arange(lower,upper)
        #Find location of maximum value within this region
        peak = np.argmax(smoothlist[i][domain]) + lower
        guess_x=peak
        #Find domain to fit the gaussian to
        #This looks for when the guassian crosses below some factor of the
        #peak amplitude
        relative_check=0.20
        tolerance=relative_check*smoothlist[i][peak]
        x=0
        while x==0:
            if smoothlist[i][guess_x] >= tolerance:
                guess_x+=-1
            else:
                lower=guess_x
                x=1
        guess_x=peak
        x=0
        while x==0:
            if smoothlist[i][guess_x] >= tolerance:
                guess_x+=1
            else:
                upper=guess_x
                x=1
        newdomain = np.arange(lower,upper)
        newdomainlist.append(newdomain)
        #Initalize Guess parameters
        guess = [50000,peak,100,0,0]
        try:
            #Fit function to gaussian as defined above within domain
            values, covarience = cf(gaussian,newdomain,smoothlist[i][newdomain],p0=guess)
            values[2] = np.abs(values[2])
            valueslist.append(values)
            fit = gaussian(newdomain,values[0],values[1],values[2],values[3],values[4])
            fitlist.append(fit)
            #Calculate R2 value
            residual = np.sum((smoothlist[i][newdomain] - fit)**2)
            total = np.sum((smoothlist[i][newdomain]-np.mean(smoothlist[i][newdomain]))**2)
            r2 = 1 - (residual/total)
            r2list.append(r2)
        except (RuntimeError, TypeError):
            #In case of error, populate with 0s that will be filtered out later
            valueslist.append([0,0,0,0,0])
            fitlist.append(np.zeros(len(newdomain)))
            r2list.append(0)
    #Make into numpy arrays in order allow easier manipulation
    newdomainlist=np.array(newdomainlist)
    valueslist=np.array(valueslist)
    fitlist=np.array(fitlist)
    r2list=np.array(r2list)
    
    #Initalize empty arrays to populate with only good R2 fits
    goodtrial=[]
    goodpositive=[]
    gooddomain=[]
    goodvalues=[]
    goodfit=[]
    goodr2=[]
    
    #Populate arrays with good R2 fits
    for i in range(len(Specs)):
        if r2list[i] >= 0.95:
            goodpositive.append(Specs[i])
            gooddomain.append(newdomainlist[i])
            goodvalues.append(valueslist[i])
            goodfit.append(fitlist[i])
            goodr2.append(r2list[i])
            goodtrial.append(TrialNum[i])
    
    #Split good values into their respective quantities
    SASEPara = np.transpose(goodvalues)
    Amp = SASEPara[0]
    Wave = SASEPara[1]
    Sig = SASEPara[2]
    Xterm = SASEPara[3]
    Constant = SASEPara[4]
    
    #Create Dictionary in which to later convert to a dataframe
    gooddict = {'Spec Number':goodtrial,'Shot Spec':goodpositive,
                'SASE Domain':gooddomain,'SASE Gaussian Fit':goodfit,
                'SASE R2':goodr2,'SASE Amplitude':Amp,'SASE Energy':Wave,
                'SASE Sigma':Sig,'SASE Linear':Xterm,'SASE Constant':Constant}
    
    GoodData = pd.DataFrame.from_dict(gooddict)
    GoodData.to_pickle('./GoodData/SASEData'+str(dataset)+'.pkl')
    return GoodData


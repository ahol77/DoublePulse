# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:55:31 2019

@author: aholm
"""

import numpy as np
from scipy.optimize import curve_fit as cf
import pandas as pd

def gaussian(x, amp, cen, sig, lin, lift):
    return amp * np.exp(-(x-cen)**2 / (2*sig**2)) + lin*x + lift

def FitSeed(dataset,specs):
    #Fit the seeded region of the spectrum to a Gaussian
    #Initalize lists to populate with fits
    newdomainlist=[]
    valueslist=[]
    fitlist=[]
    r2list=[]
    
    #Establish minimum peak in which to accept a Gaussian fit
    #A smaller value accepts more initial fits that may get removed later
    minimum_peak=20000
    
    for i in range(len(specs)):
        #Set bounds to check for maximum to begin fitting process
        lower=1200
        upper=1400
        domain = np.arange(lower,upper)
        #Find location of maximum value within this region
        peak = np.argmax(specs[i][domain]) + lower
        guess_x=peak
        #Find domain to fit the gaussian to
        #This looks for when the guassian crosses below some factor of the
        #peak amplitude
        relative_check=0.10
        tolerance=relative_check*specs[i][peak]
        x=0
        while x==0:
            if specs[i][guess_x] >= tolerance:
                guess_x+=-1
            else:
                lower=guess_x
                x=1
        guess_x=peak
        x=0
        while x==0:
            if specs[i][guess_x] >= tolerance:
                guess_x+=1
            else:
                upper=guess_x
                x=1
        newdomain = np.arange(lower,upper)
        newdomainlist.append(newdomain)
        #Initalize Guess parameters
        guess = [200000,peak,10,0,0]
        try:
            #Fit function to gaussian as defined above within domain
            values, covarience = cf(gaussian,newdomain,specs[i][newdomain],p0=guess)
            if values[0] >= minimum_peak:
                #As sigma is squared in equation, just make sure it is positive
                values[2] = np.abs(values[2])
                valueslist.append(values)
                #Calculate fit in order to save for later
                fit = gaussian(newdomain,values[0],values[1],values[2],values[3],values[4])
                fitlist.append(fit)
                #Calculate R2 value
                residual = np.sum((specs[i][newdomain] - fit)**2)
                total = np.sum((specs[i][newdomain]-np.mean(specs[i][newdomain]))**2)
                r2 = 1 - (residual/total)
                r2list.append(r2)
            else:
                #Populate with 0s that will be filtered out later
                valueslist.append([0,0,0,0,0])
                fitlist.append(np.zeros(len(newdomain)))
                r2list.append(0)
        except (RuntimeError,TypeError):
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
    goodpositive=[]
    gooddomain=[]
    goodvalues=[]
    goodfit=[]
    goodr2=[]
    goodtrial=[]
    
    badspec=[]
    
    #Populate arrays with good R2 fits
    for i in range(len(specs)):
        if r2list[i] >= 0.95:
            goodpositive.append(specs[i])
            gooddomain.append(newdomainlist[i])
            goodvalues.append(valueslist[i])
            goodfit.append(fitlist[i])
            goodr2.append(r2list[i])
            goodtrial.append(i)
        else:
            badspec.append(specs[i])
    
    #Split good values into their respective quantities
    SeedPara = np.transpose(goodvalues)
    Amp = SeedPara[0]
    Wave = SeedPara[1]
    Sig = SeedPara[2]
    Xterm = SeedPara[3]
    Constant = SeedPara[4]
    
    #Create Dictionary in which to later convert to a dataframe
    gooddict = {'Spec Number':goodtrial,'Shot Spec':goodpositive,
                'Seed Domain':gooddomain,'Seed Gaussian Fit':goodfit,
                'Seed R2':goodr2,'Seed Amplitude':Amp,'Seed Energy':Wave,
                'Seed Sigma':Sig,'Seed Linear':Xterm,'Seed Constant':Constant}
    GoodData = pd.DataFrame.from_dict(gooddict)
    
    baddict = {'Shot Spec':badspec}
    BadData = pd.DataFrame.from_dict(baddict)
    
    GoodData.to_pickle('./GoodData/SeedData'+str(dataset)+'.pkl')
    BadData.to_pickle('./BadSeedData/BadSeedData'+str(dataset)+'.pkl')
    
    return GoodData
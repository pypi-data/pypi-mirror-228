# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 21:10:39 2023

@author: lluri
"""
import numpy as np
from cbwe import cbwe
def half(q,I,dI):
    '''
    and merges all pairs of adjacent points in q, 
    so that there are half as many q points with 
    correspondingly smaller error bars.  
    '''
    nlen = int(2*np.floor(len(q)/2))
    q = q[0:nlen]
    I = I[0:nlen]
    dI = dI[0:nlen]
    eve = np.arange(0,nlen-1,2).astype(int)
    odd = np.arange(1,nlen,2).astype(int)
    qout = (q[eve]+q[odd])/2
    Iout,dIout = cbwe(I[eve],dI[eve],I[odd],dI[odd])
    return  qout,Iout,dIout 
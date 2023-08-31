# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:40:11 2022

@author: lluri
"""
from numpy import linspace,exp
import numpy as np
from scipy.special import erf
def get_prof(amp, zcen, sig):
    '''
    get_prof(zcen, amp, sig)
    function to return real space profile from
    arrays of zcenters, amplitudes and widths
    '''
    zspan = max(zcen) - min(zcen)
    zmin = min(zcen)-2*zspan
    zmax = max(zcen) +2*zspan
    zrange = linspace(zmin, zmax, 2**10)
    prof = zrange*0
    for thisz, thisa, thiss in zip(zcen, amp, sig):
        prof += thisa*exp(-(zrange-thisz)**2/2/thiss**2)
    return zrange, prof
def get_dprof(amp, zcen, sig):
    '''
    get_prof(zcen, amp, sig)
    function to return real space profile from
    arrays of zcenters, amplitudes and widths
    '''
    zspan = max(zcen) - min(zcen)
    zmin = min(zcen)-2*zspan
    zmax = max(zcen) +2*zspan
    zrange = linspace(zmin, zmax, 2**10)
    prof = zrange*0
    lasta = amp[0]
    prof = np.abs(prof) + lasta
    for  thisz, thisa, thiss  in zip(zcen, amp[1:], sig):
        prof += (thisa-lasta)*(erf((thisz-zrange)/thiss)+1)/2
        lasta = thisa
    return zrange, prof
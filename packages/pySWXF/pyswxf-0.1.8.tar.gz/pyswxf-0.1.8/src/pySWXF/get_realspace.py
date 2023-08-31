# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 14:52:35 2022

@author: lluri
"""

def get_realspace(params,E0):
    D_H = params['D_H'].value
    D_B = params['D_B'].value
    D_M = params['D_M'].value
    D_A = (D_B -2*D_H-D_M)/2
    rho_H = params['rho_H'].value
    rho_A = params['rho_A'].value
    sig = params['sig'].value
    sig_SiO2 = params['sig_SiO2'].value
    zcen, sig_i, layers = get_layers(sig_SiO2,rho_H,rho_A,D_A,D_H,D_M,sig)
    amp = []
    for lay in layers:
        amp = np.append(amp,rho_to_rhoe(lay[0],lay[1],E0)*scc.angstrom**3)
    zrange, prof = get_dprof(amp, zcen, sig_i)
    return zrange, prof,amp,zcen,sig_i,layers
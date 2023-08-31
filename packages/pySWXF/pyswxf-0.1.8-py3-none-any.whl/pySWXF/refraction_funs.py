import sys
import scipy.constants as scc
from numpy import sqrt, tile, transpose, pi, sin, exp, zeros
from numpy import linspace
from numpy import sum as nsum
from numpy import abs as nabs
sys.path.append(r'C:\Users\lluri\Anaconda3\envs\lbl\XrayDB-master\python\xraydb')
from xraydb import XrayDB
xdb = XrayDB()
pc = scc.physical_constants
r_0 = pc["classical electron radius"][0]
q_e = pc["elementary charge"][0]
N_A = pc["Avogadro constant"][0]
h = pc["Planck constant"][0]
c = pc["speed of light in vacuum"][0]

def n_elem(elem,E): 
    # E given in eV 
    rho = xdb.density(elem)
    f = xdb.atomic_number(elem) + xdb.f1_chantler(elem,E) - xdb.f2_chantler(elem,E)*1j
    Ne = rho*f*N_A*1e6/xdb.molar_mass(elem)    
    lam = h*c/q_e/E
    n = 1.0 - r_0*Ne*lam**2/2.0/pi
    return n
    
def n_water(E):
    # E given in eV
    f_H = xdb.atomic_number('H') + xdb.f1_chantler('H',E) -1j*xdb.f2_chantler('H',E)
    f_O = xdb.atomic_number('O') + xdb.f1_chantler('O',E) -1j*xdb.f2_chantler('O',E)
    A_H = xdb.molar_mass('H') 
    A_O = xdb.molar_mass('O') 
    f = 2*f_H+f_O
    A = A_O+2*A_H
    rho = 1.0
    Ne = rho*f*N_A*1e6/A    
    lam = h*c/q_e/E
    n = 1.0 - r_0*Ne*lam**2/2.0/pi
    return n
    
def n_SiO2(E):
    # E given in eV
    f1_Si = xdb.atomic_number('Si') + xdb.f1_chantler('Si',E) -1j*xdb.f2_chantler('Si',E)
    f1_O = xdb.atomic_number('O') + xdb.f1_chantler('O',E) -1j*xdb.f2_chantler('O',E)
    A_Si = xdb.molar_mass('Si') 
    A_O = xdb.molar_mass('O') 
    f = f1_Si+2*f1_O
    A = 2*A_O+A_Si
    rho = 2.203
    Ne = rho*f*N_A*1e6/A    
    lam = h*c/q_e/E
    n = 1.0 - r_0*Ne*lam**2/2.0/pi
    return n

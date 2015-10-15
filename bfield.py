# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 15:59:20 2014

@author: mrea1g12
"""
###############################################################################
#IMPORTS

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

###############################################################################
#FORMATTING

font={'size' : 19}
matplotlib.rc('font', **font)

###############################################################################
#DEFINITIONS

def solenoid(N, I, l, R, z, D=0):
    
    k = 4 * np.pi * 1e-7 *N*I/(4*l)
    z_plus = (z - D + l)/np.sqrt((z - D + l)**2 + R**2)
    z_minus = (z - D - l)/np.sqrt((z - D - l)**2 + R**2)      
    
    return k*(z_plus - z_minus)

position_1 = -0.07
position_2 = 0.07
n_steps = 100
config = "anti-helmholtz"

separations = np.linspace(0.14, 0.5, num=1)

fig = plt.figure()
ax = fig.add_subplot(111)

z_theoretical = np.linspace(position_1, position_2, n_steps + 1)
id_coils = [100, 2, 0.04, 0.12, z_theoretical]
b_list_theory = []
units = "G"
conversion = {"T":1, "mT":1e3, "G":1e4}

###############################################################################
#CALCULATIONS

if config == "helmholtz":
    for d in separations:
        b_list_theory.append(solenoid(*id_coils, D=d) + solenoid(*id_coils, D=-d))
elif config == "anti-helmholtz":
    for d in separations:
        b_list_theory.append(solenoid(*id_coils, D=d) - solenoid(*id_coils, D=-d))

if units in conversion:
    factor = conversion[units]
else:
    units = "T"
    factor = 1

###############################################################################
#DATA OUTPUT

for index, item in enumerate(b_list_theory):
    ax.plot(z_theoretical, item*factor, label="%.2fm separation" % separations[index])
    print "|{0:.2f}m separation\t|mean {1:.2f}{2}\t|STD {3:.2f}{2}|".format(
    separations[index], np.mean(item)*factor, units, np.std(item)*factor)

ax.set_xlabel("$z$ (m)")
ax.set_ylabel("$B_z$ (%s)" % units)
plt.legend(loc="best")
plt.show()

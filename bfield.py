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
    
    # Takes parameters:
    #    N = number of solenoid turns
    #    I = current in coil
    #    l = coil depth
    #    R = coil radius
    #    z = probe position along axis
    #    D = coil separation along axis

    # First line calculates a constant premultiplier based on
    # the Biot-Savart law.    
    k = 4 * np.pi * 1e-7 *N*I/(4*l)
    
    # Next two lines calculate the positive and negative components
    # of z displacement term
    z_plus = (z - D + l)/np.sqrt((z - D + l)**2 + R**2)
    z_minus = (z - D - l)/np.sqrt((z - D - l)**2 + R**2)      
    
    # Finally, put it all together
    return k*(z_plus - z_minus)
    
# Declare initial positions of coils relative to midpoint
position_1 = -0.1
position_2 = 0.1

# Set granularity of simulation (number of probe points on z axis)
n_steps = 100

# Set to either "helmholtz" or "antihelmholtz" depending on desire
# for either uniform or quadrupole field
config = "helmholtz"

# Calculates required positions of coils (default is num=1, which will only
# calculate B field for initial positions)
separations = np.linspace(position_2 - position_1, 0.5, num=1)

# Set up plotting
fig = plt.figure()
ax = fig.add_subplot(111)

# Figure out exactly where the sample points should be
z_theoretical = np.linspace(position_1, position_2, n_steps + 1)

# This list defines the coil setup and parameters:
#    [Number of turns, current through each, depth, radius, z probe positions]
id_coils = [397, 1.5, 0.04, 0.1515, z_theoretical]

# Makes a container for the theoretical values
b_list_theory = []

# Set this to the units you want:
#    "G" = Gauss
#    "T" = Tesla
#    "mT" = milliTesla
units = "mT"

# This line defines the units you refer to above.
conversion = {"T":1, "mT":1e3, "G":1e4}

###############################################################################
#CALCULATIONS

# For a given configuration, set the coil orientation and calculate B at every
# given z position
if config == "helmholtz":
    for d in separations:
        b_list_theory.append(solenoid(*id_coils, D=d) + solenoid(*id_coils, D=-d))
        
elif config == "anti-helmholtz":
    for d in separations:
        b_list_theory.append(solenoid(*id_coils, D=d) - solenoid(*id_coils, D=-d))

# Apply conversion factor with failsafe to make sure Tesla doesn't convert
if units in conversion:
    factor = conversion[units]
else:
    units = "T"
    factor = 1

###############################################################################
#DATA OUTPUT

# Create a plot for every separation requested
for index, item in enumerate(b_list_theory):
    ax.plot(z_theoretical, item*factor, label="%.2fm separation" % separations[index])
    print "|{0:.2f}m separation\t|mean {1:.2f}{2}\t|STD {3:.2f}{2}|".format(
    separations[index], np.mean(item)*factor, units, np.std(item)*factor)
    
# Make the plots pretty
ax.set_xlabel("$z$ (m)")
ax.set_ylabel("$B_z$ (%s)" % units)
plt.legend(loc="best")
#plt.axis([position_1, position_2, 0, 0.01])
plt.show()
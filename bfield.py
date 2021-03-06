# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 15:59:20 2014

Updated with better comments on Thu Oct 15 15:12:33 2015

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
    z_plus = (z - D/2 + l)/np.sqrt((z - D/2 + l)**2 + R**2)
    z_minus = (z - D/2 - l)/np.sqrt((z - D/2 - l)**2 + R**2)      
    
    # Finally, put it all together
    return k*(-z_plus + z_minus)
    
# Declare initial positions of coils relative to midpoint
position_1 = -4e-3
position_2 = 4e-3
d = position_2 - position_1

# Set granularity of simulation (number of probe points on z axis)
n_steps = 1000

# Set to either "helmholtz" or "antihelmholtz" depending on desire
# for either uniform or quadrupole field
config = "antihelmholtz"

# Set up plotting
fig = plt.figure()
ax_B = fig.add_subplot(111)
ax_g = ax_B.twinx()

# Figure out exactly where the sample points should be
z_theoretical = np.linspace(2*position_1, 2*position_2, n_steps + 1)

# This list defines the coil setup and parameters:
#    [Number of turns, current through each, depth, radius, z probe positions]

pcb_coils = [20, 0.1, 0.2e-3, 12e-3, z_theoretical]
id_coils = pcb_coils

# Set this to the units you want:
#    "G" = Gauss
#    "T" = Tesla
#    "mT" = milliTesla
units = "G"

# This line defines the units you refer to above.
conversion = {"T":1, "mT":1e3, "G":1e4, "mG":1e7}

###############################################################################
#CALCULATIONS

# For a given configuration, set the coil orientation and calculate B at every
# given z position
if config == "helmholtz":
    b_theory = solenoid(*id_coils, D=d) + solenoid(*id_coils, D=-d)
        
elif config == "antihelmholtz":
        b_theory = solenoid(*id_coils, D=d) - solenoid(*id_coils, D=-d)

# Apply conversion factor with failsafe to make sure Tesla doesn't convert
if units in conversion:
    factor = conversion[units]
else:
    units = "T"
    factor = 1

b_gradient= np.diff(b_theory)/np.diff(z_theoretical)
###############################################################################
#DATA OUTPUT

# Create a plot
field, = ax_B.plot(z_theoretical, b_theory*factor, 'r', lw=5)
grad, = ax_g.plot(z_theoretical[1:], b_gradient*factor/100, 'gray', lw=5)
#expt, = ax_B.plot(z_experimental, b_experimental, ".g")
    
# Make the plot pretty
ax_B.set_xlabel("$z$ (m)")
ax_B.set_ylabel("$B_z$ (%s)" % units)
ax_g.set_ylabel("$\partial_zB$ (%s/cm)" % units)
fig.legend([field, grad],#, expt],
           ["B field %.2em separation" % d,
           "Gradient %.2em separation" % d,
           "Experimental B field data"],
           loc = "upper center")
           
plt.show()
plt.savefig("b-field.png")

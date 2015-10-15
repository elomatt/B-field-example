# B-field-example
Example code showing how to simulate (pair of) solenoid magnetic field.

Code should be self-explanatory, and is written to accompany Stand-Alone experiment B in PHY1017 at University of Southampton.

Any questions should be directed to the author:

Matt Aldous:
    e : matt.aldous@soton.ac.uk
    
    t : 23931
    
    a : Building 46, room 1027
    
    
    
Basic usage instructions:

  1) Read and understand the definition of the function "solenoid" (on line 23), with reference to the formulation of the Biot-Savart law in your student text.
  
  2) Edit the values of "position_1" and "position_2" (on lines 31 and 32) to reflect the positions of the solenoids relative to a reference point (e.g. for a 20cm separation, set these values to -0.1 and 0.1)
  
  3) Set the number of steps along the z-axis at which you want to sample by editing n_steps (line 33)
  
  4) Edit "id_coils" (line 42) to match the parameters of your coils.
  
  5) Set the units you wish to plot in. Gauss is recommended, but milliTesla and Tesla are other options available
  
  6) Run the script in a python environment and use the output to compare to your characterisation of the coils.
  

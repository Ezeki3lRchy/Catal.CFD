import numpy as np
import solver
import importlib
import plotting as g
importlib.reload(g)

importlib.reload(solver)
from solver import calculate

# Define the range of mole fractions for O
CO_values = [0.1, 0.3, 0.5, 0.7, 0.9] # Example values for O's mole fraction

# Constant pressure
pressure = 1000  # Example pressure in Pa

# Temperature range
temperatures = np.linspace(300, 5000, 1000)  # Example temperature range from 300K to 3750K

# Path to the parameter file
param_file = 'sio2_para.py'

results_list = []

# Iterate over the values of C0
for CO in CO_values:
    # Calculate CN based on C0
    
    # Perform the calculation for the current value of C0 and CN
    results = calculate(temperatures, [pressure], param_file, C_O=CO)
    results_list.append(results)

# Plot the results
g.plot_gamma_ratio(results_list, CO_values)
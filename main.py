import numpy as np
from solver import calculate
import postprocess as g
import time

temperatures = np.linspace(300, 2000, 1000)  # Example temperature range from 300K to 3000K

pressures = [11, 110, 550, 1100, 11000]  # Example pressures in Pa
param_file = 'Sio2_para.py'  # Path to the parameter file

results_list = []
# Track total runtime
total_start = time.time()
    
for pressure in pressures:
    results = calculate(temperatures, [pressure], param_file)
    results_list.append(results)

g.plot_multigamma(results_list, [1100])

# Print total runtime
total_end = time.time()
print(f"Total runtime: {total_end - total_start:.2f} seconds")

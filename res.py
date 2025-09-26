import numpy as np
from solver import calculate
import postprocess as g

temperatures = np.linspace(300, 3000, 10)  # Example temperature range from 300K to 3000K
pressures = [10, 100, 1000]  # Example pressures in Pa
param_file = 'test_para.py'  # Path to the parameter file

results_list = []

for pressure in pressures:
    results = calculate(temperatures, [pressure], param_file)
    results_list.append(results)

# Print available temperature and pressure values
for i, results in enumerate(results_list):
    print(f"Results for pressure {pressures[i]} Pa:")
    print("Temperatures:", results['T'].values)
    print("Pressures:", results['P'].values)

# Plot residuals for a specific temperature and pressure
specific_T = 1500  # Example specific temperature
specific_P = 100  # Example specific pressure


# Plot the residuals
g.plot_residuals_single_point(results_list[1], specific_T, specific_P)
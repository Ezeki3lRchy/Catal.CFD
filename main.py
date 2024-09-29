import numpy as np
from solver import calculate
import plotting as g

temperatures = np.linspace(300, 3000, 10)  # Example temperature range from 300K to 3000K
pressures = [10, 100, 1000]  # Example pressures in Pa
param_file = 'test_para.py'  # Path to the parameter file

results_list = []

for pressure in pressures:
    results = calculate(temperatures, [pressure], param_file)
    results_list.append(results)

g.plot_gamma_OO(results_list, pressures)
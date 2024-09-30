import numpy as np
import solver
import importlib
import plotting as g
importlib.reload(g)

importlib.reload(solver)
from solver import calculate





temperatures = np.linspace(300, 3700, 1000)  # Example temperature range from 300K to 3000K
pressures = [11, 110, 550, 1100, 2200]  # Example pressures in Pa
param_file = 'sio2_para.py'  # Path to the parameter file

results_list = []

for pressure in pressures:
    results = calculate(temperatures, [pressure], param_file)
    results_list.append(results)


g.plot_gamma_NN(results_list, pressures)
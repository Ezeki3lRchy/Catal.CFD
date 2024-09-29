import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import importlib.util

def load_parameters(param_file):
    spec = importlib.util.spec_from_file_location("params", param_file)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)
    return params


def calculate(temperatures, pressures, param_file):

    # Load parameters from the specified file
    params = load_parameters(param_file)

    # Initialize a dictionary to store the results
    res_dict = {
        "theta_O": [],
        "theta_N": [],
        "T": [],
        "P": [],
        "x": [],
        "gamma_OO": [],
        "gamma_NN": [],
        "gamma_ON": [],
        "gamma_NO": [],
        "omega_ad_O": [],
        "omega_ad_N": [],
        "omega_ER_OO": [],
        "omega_ER_NN": [],
        "omega_ER_ON": [],
        "omega_ER_NO": [],
        "omega_LH_OO": [],
        "omega_LH_NN": [],
        "omega_LH_NO": [],
        "omega_des_O": [],
        "omega_des_N": [],
        "residuals": []  # Add a new key for residuals
    }

    # Main Loop
    for T in temperatures:
        for p in pressures:
            x = 1000 / T  # invT

            # partial pressure
            p_O = p * params.C0  
            p_N = p * params.CN

            # Flux of hitting surface
            n_O = p_O / (np.sqrt(2 * np.pi * params.mass_O * params.kB * T))  
            n_N = p_N / (np.sqrt(2 * np.pi * params.mass_N * params.kB * T))

            # ER
            gamma_star_OO = params.P_erOO * np.exp(-params.Q_erOO / (params.kB * T))
            gamma_star_NN = params.P_erNN * np.exp(-params.Q_erNN / (params.kB * T))
            gamma_star_ON = params.P_erON * np.exp(-params.Q_erON / (params.kB * T))
            gamma_star_NO = params.P_erNO * np.exp(-params.Q_erNO / (params.kB * T))

            # LH
            v_O = (params.cA / params.delta) * np.sqrt(np.pi * params.kB * T / (2 * params.mass_O))
            v_N = (params.cA / params.delta) * np.sqrt(np.pi * params.kB * T / (2 * params.mass_N))

            # OH
            theta_OH = params.AA * (1.0 - np.exp(-params.E_OH / params.Na / T))

            # Reaction Functions
            omega_ad_O = lambda theta_O, theta_N: params.s_O * (1 - theta_O - theta_N - theta_OH) * n_O
            omega_ad_N = lambda theta_O, theta_N: params.s_N * (1 - theta_O - theta_N - theta_OH) * n_N

            omega_ER_OO = lambda theta_O: 1 * gamma_star_OO * theta_O * n_O
            omega_ER_NN = lambda theta_N: 1 * gamma_star_NN * theta_N * n_N
            omega_ER_ON = lambda theta_N: 1 * gamma_star_ON * theta_N * n_O
            omega_ER_NO = lambda theta_O: 1 * gamma_star_NO * theta_O * n_N

            omega_LH_OO = lambda theta_O: 2.0 * v_O * params.nsite * theta_O**2 * np.exp(-params.Q_lhOO / (params.kB * T))
            omega_LH_NN = lambda theta_N: 2.0 * v_N * params.nsite * theta_N**2 * np.exp(-params.Q_lhNN / (params.kB * T))
            omega_LH_NO = lambda theta_O, theta_N: (v_O + v_N) * params.nsite * theta_N * theta_O * np.exp(-params.Q_lhNO / (params.kB * T))

            omega_des_O = lambda theta_O: 1 * params.nsite * theta_O * (params.kB * T / params.h) * np.exp(-params.Qa_O / (params.kB * T))
            omega_des_N = lambda theta_N: 1 * params.nsite * theta_N * (params.kB * T / params.h) * np.exp(-params.Qa_N / (params.kB * T))

            # Steady State Equations
            def SysEqs(initial_guess):
                theta_O, theta_N = initial_guess
                eq1 = omega_ad_O(theta_O, theta_N) - omega_ER_OO(theta_O) - omega_ER_NO(theta_O) - omega_LH_NO(theta_O, theta_N) - omega_LH_OO(theta_O) - omega_des_O(theta_O)
                eq2 = omega_ad_N(theta_O, theta_N) - omega_ER_NN(theta_N) - omega_ER_ON(theta_N) - omega_LH_NO(theta_O, theta_N) - omega_LH_NN(theta_N) - omega_des_N(theta_N)
                return [eq1, eq2]

            # Solve the system of equations
            initial_guess = [0.5, 0.5]
            theta, infodict, ier, msg = fsolve(SysEqs, initial_guess, full_output=True)

            # Post-processing with final theta values
            theta_O, theta_N = theta[0], theta[1]

            # Calculate omega values based on theta
            omega_ad_O_val = omega_ad_O(theta_O, theta_N)
            omega_ad_N_val = omega_ad_N(theta_O, theta_N)

            omega_ER_OO_val = omega_ER_OO(theta_O)
            omega_ER_NN_val = omega_ER_NN(theta_N)
            omega_ER_ON_val = omega_ER_ON(theta_N)
            omega_ER_NO_val = omega_ER_NO(theta_O)

            omega_LH_OO_val = omega_LH_OO(theta_O)
            omega_LH_NN_val = omega_LH_NN(theta_N)
            omega_LH_NO_val = omega_LH_NO(theta_O, theta_N)

            omega_des_O_val = omega_des_O(theta_O)
            omega_des_N_val = omega_des_N(theta_N)

            # Calculate gamma values based on omega
            gamma_OO = (omega_LH_OO_val + 2 * omega_ER_OO_val) / n_O
            gamma_NN = (omega_LH_NN_val + 2 * omega_ER_NN_val) / n_N
            gamma_ON = (omega_LH_NO_val + omega_ER_NO_val + omega_ER_ON_val) / n_O
            gamma_NO = (omega_LH_NO_val + omega_ER_NO_val + omega_ER_ON_val) / n_N

            # Append results to the dictionary
            res_dict["theta_O"].append(theta_O)
            res_dict["theta_N"].append(theta_N)
            res_dict["T"].append(T)
            res_dict["P"].append(p)
            res_dict["x"].append(x)
            res_dict["gamma_OO"].append(gamma_OO)
            res_dict["gamma_NN"].append(gamma_NN)
            res_dict["gamma_ON"].append(gamma_ON)
            res_dict["gamma_NO"].append(gamma_NO)
            res_dict["omega_ad_O"].append(omega_ad_O_val)
            res_dict["omega_ad_N"].append(omega_ad_N_val)
            res_dict["omega_ER_OO"].append(omega_ER_OO_val)
            res_dict["omega_ER_NN"].append(omega_ER_NN_val)
            res_dict["omega_ER_ON"].append(omega_ER_ON_val)
            res_dict["omega_ER_NO"].append(omega_ER_NO_val)
            res_dict["omega_LH_OO"].append(omega_LH_OO_val)
            res_dict["omega_LH_NN"].append(omega_LH_NN_val)
            res_dict["omega_LH_NO"].append(omega_LH_NO_val)
            res_dict["omega_des_O"].append(omega_des_O_val)
            res_dict["omega_des_N"].append(omega_des_N_val)
            res_dict["residuals"].append(infodict['fvec'])  # Store the residuals

    # Convert the dictionary to a pandas DataFrame
    res_df = pd.DataFrame(res_dict)
    return res_df
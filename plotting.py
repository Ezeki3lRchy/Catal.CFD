import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, LogLocator

# Define the path to the Times New Roman font on Windows
font_properties = FontProperties(fname='C:\\Windows\\Fonts\\times.ttf')
TICK_LABEL_SIZE = 16  # Increased tick label size
# Update rcParams to use Times New Roman for all text elements

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman'] + rcParams['font.serif']
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Times New Roman'

def plot_multigamma(res, x_label=r'1000 / T  $[\mathrm{K}^{-1}]$', y_label='Recombination coefficient'):
    plt.figure(figsize=(10, 6))
    plt.semilogy(res['x'], res['gamma_OO'], label='gamma_OO', linewidth=1)
    plt.semilogy(res['x'], res['gamma_NN'], label='gamma_NN', linewidth=1)
    plt.semilogy(res['x'], res['gamma_ON'], label='gamma_ON', linewidth=1)
    plt.semilogy(res['x'], res['gamma_NO'], label='gamma_NO', linewidth=1)

    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)

    legend = plt.legend(fontsize=16, frameon=True, framealpha=1, edgecolor='black', fancybox=False)
    legend.get_frame().set_linewidth(1)  # Set the legend border thickness

    # Set the linewidth of the x and y axes
    plt.gca().spines['top'].set_linewidth(2)
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['right'].set_linewidth(2)

    # Enable minor ticks
    plt.gca().minorticks_on()

    # Automatically adjust minor ticks to have one minor tick between each pair of major ticks on x-axis
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))

    # Set minor ticks for y-axis on a logarithmic scale
    plt.gca().yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))

    # Set font properties for tick labels and make ticks inline
    plt.gca().tick_params(axis='both', which='major', direction='in', length=6, width=1.5, pad=10)
    plt.gca().tick_params(axis='both', which='minor', direction='in', length=3, width=1, pad=10)
    plt.gca().tick_params(axis='x', which='both', top=True, bottom=True)
    plt.gca().tick_params(axis='y', which='both', left=True, right=True)

    plt.grid(which='both', linestyle='--', linewidth=1)  # Set grid lines to be dashed

    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontproperties(font_properties)
        label.set_fontsize(TICK_LABEL_SIZE)  # Set the font size for tick labels

    plt.show()

def plot_gamma_OO(results_list, pressures, x_label=r'1000 / T  $[\mathrm{K}^{-1}]$', y_label='Gamma_OO Values', title='Gamma_OO Values vs. Inverse Temperature'):
    plt.figure(figsize=(10, 6))
    
    for results, pressure in zip(results_list, pressures):
        plt.semilogy(results['x'], results['gamma_OO'], label=f'Pressure: {pressure} Pa')

    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.title(title, fontsize=20)
    plt.legend(fontsize=16, frameon=True, framealpha=1, edgecolor='black', fancybox=False)
    plt.grid(which='both', linestyle='--', linewidth=1)  # Set grid lines to be dashed

    # Set the axis range
    plt.xlim([0.3, 3])
    plt.ylim([1e-6, 1e0])

    # Set the linewidth of the x and y axes
    plt.gca().spines['top'].set_linewidth(2)
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['right'].set_linewidth(2)

    # Enable minor ticks
    plt.gca().minorticks_on()

    # Automatically adjust minor ticks to have one minor tick between each pair of major ticks on x-axis
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))

    # Set minor ticks for y-axis on a logarithmic scale
    plt.gca().yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))

    # Set font properties for tick labels and make ticks inline
    plt.gca().tick_params(axis='both', which='major', direction='in', length=6, width=1.5, pad=10)
    plt.gca().tick_params(axis='both', which='minor', direction='in', length=3, width=1, pad=10)
    plt.gca().tick_params(axis='x', which='both', top=True, bottom=True)
    plt.gca().tick_params(axis='y', which='both', left=True, right=True)

    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontproperties(font_properties)
        label.set_fontsize(TICK_LABEL_SIZE)  # Set the font size for tick labels

    plt.show()


def plot_residuals_single_point(results, T, P):
    # Find the index of the specific temperature and pressure
    index = None
    for i in range(len(results['T'])):
        if results['T'][i] == T and results['P'][i] == P:
            index = i
            break
    
    if index is None:
        print(f"No results found for T={T} and P={P}")
        return

    residuals = np.array(results['residuals'][index])
    iterations = np.arange(len(residuals))  # Create an array of iterations

    plt.plot(iterations, residuals, label=f'T={T} K, P={P} Pa')
    plt.xlabel('Iteration')
    plt.ylabel('Residual')
    plt.title('Residuals from fsolve')
    plt.legend()
    plt.show()

def plot_gamma_NN(results_list, pressures):
    for i, results in enumerate(results_list):
        inverse_T = 1000 / results['T']
        plt.semilogy(inverse_T, results['gamma_NN'], label=f'P={pressures[i]} Pa')
    
    plt.xlabel('1000 / Temperature (1/K)')
    plt.ylabel('Gamma NN')
    plt.title('Gamma NN vs 1000/T')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()
    
def save_results_to_csv(results_list, pressures, filename_prefix='results'):
    for i, results in enumerate(results_list):
        pressure = pressures[i]
        filename = f"{filename_prefix}_P{pressure}.csv"
        results.to_csv(filename, index=False)
        print(f"Results for P={pressure} Pa saved to {filename}")

def plot_gamma_OO_3d(results_list, pressures):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for i, results in enumerate(results_list):
        T = results['T']
        P = [pressures[i]] * len(T)
        gamma_OO = results['gamma_OO']
        ax.plot(T, P, gamma_OO, label=f'P={pressures[i]} Pa')
    
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Pressure (Pa)')
    ax.set_zlabel('Gamma OO')
    ax.set_title('Gamma OO vs Temperature and Pressure')
    ax.legend()
    plt.show()
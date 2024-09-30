import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
# Define the path to the Times New Roman font on Windows
font_properties = FontProperties(fname='C:\\Windows\\Fonts\\times.ttf')
TICK_LABEL_SIZE = 16  # Increased tick label size

# Update rcParams to use Times New Roman for all text elements
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman'] + rcParams['font.serif']
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Times New Roman'

xlabel1 = r'1000/T $[\mathrm{K}^{-1}]$'
save_path = 'E:\\Project\\cross-sectional project'
def apply_plot_formatting(x_label, y_label, title=None):
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    if title:
        plt.title(title, fontsize=20)
    plt.legend(fontsize=16, 
               frameon=True, 
               framealpha=1, 
               edgecolor='black', 
               fancybox=False,
               borderpad=0.3, labelspacing=0.2
               )
    plt.grid(which='both', linestyle='--', linewidth=1)  # Set grid lines to be dashed

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
    plt.gca().tick_params(axis='both', which='major', direction='in', length=6, width=1.5, pad=5)
    plt.gca().tick_params(axis='both', which='minor', direction='in', length=3, width=1, pad=5)
    plt.gca().tick_params(axis='x', which='both', top=True, bottom=True)
    plt.gca().tick_params(axis='y', which='both', left=True, right=True)

    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontproperties(font_properties)
        label.set_fontsize(TICK_LABEL_SIZE)  # Set the font size for tick labels


def plot_multigamma(results_list, pressures, y_label='Recombination coefficient'):
    plt.figure(figsize=(10, 6))
    
    for results, pressure in zip(results_list, pressures):
        plt.semilogy(results['x'], results['gamma_OO'], label=f'gamma_OO, P={pressure} Pa', linewidth=1)
        plt.semilogy(results['x'], results['gamma_NN'], label=f'gamma_NN, P={pressure} Pa', linewidth=1)
        plt.semilogy(results['x'], results['gamma_ON'], label=f'gamma_ON, P={pressure} Pa', linewidth=1)
        plt.semilogy(results['x'], results['gamma_NO'], label=f'gamma_NO, P={pressure} Pa', linewidth=1)

    apply_plot_formatting(xlabel1, y_label)
    plt.savefig(f'{save_path}\\multigamma.png', dpi=1000, bbox_inches='tight')
    plt.show()

def plot_gamma_OO(results_list, pressures, 
                  y_label='Recombination coefficient', 
                  title=None):
    
    plt.figure(figsize=(8, 6))
    
    for results, pressure in zip(results_list, pressures):
        plt.semilogy(results['x'], results['gamma_OO'], label=f'Pressure: {pressure} Pa')

    apply_plot_formatting(xlabel1, y_label, title)
    plt.xlim([0.3, 1])
    plt.ylim([1e-3, 1e-1])
    plt.savefig(f'{save_path}\\gamma_OO.png', dpi=1000, bbox_inches='tight')
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
    apply_plot_formatting('Iteration', 'Residual')
    plt.savefig(f'residuals_T{T}_P{P}.png', dpi=1000, bbox_inches='tight')
    plt.show()

def plot_gamma_NN(results_list, pressures, y_label='Recombination coefficient'):
    plt.figure(figsize=(8, 6))
    
    for i, results in enumerate(results_list):
        inverse_T = 1000 / results['T']
        plt.semilogy(inverse_T, results['gamma_NN'], label=f'P={pressures[i]} Pa')
    
    apply_plot_formatting(xlabel1, y_label)
    plt.xlim([0.25, 2])
    plt.ylim([1e-4, 1e-1])

    plt.savefig(f'{save_path}\\gamma_NN.png', dpi=1000, bbox_inches='tight')
    plt.show()

def save_results_to_csv(results_list, pressures, filename_prefix='results'):
    for i, results in enumerate(results_list):
        pressure = pressures[i]
        filename = f"{filename_prefix}_P{pressure}.csv"
        results.to_csv(filename, index=False)
        print(f"Results for P={pressure} Pa saved to {filename}")

def plot_gamma_OO_3d(results_list, pressures, y_label='Recombination coefficient'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for i, results in enumerate(results_list):
        T = results['T']
        P = [pressures[i]] * len(T)
        gamma_OO = results['gamma_OO']
        ax.plot(T, P, gamma_OO, label=f'P={pressures[i]} Pa')
    
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Pressure (Pa)')
    ax.set_zlabel(y_label)
    ax.legend()
    plt.savefig(f'{save_path}\\gamma_OO_3d.png', dpi=1000, bbox_inches='tight')
    plt.show()

def plot_gamma_NO(results_list, pressures, y_label='Recombination coefficient'):
    plt.figure(figsize=(8, 6))
    



    for i, results in enumerate(results_list):
        inverse_T = 1000 / results['T']
        plt.semilogy(inverse_T, results['gamma_NO'], label=f'P={pressures[i]} Pa')
    
    apply_plot_formatting(xlabel1, y_label)
    plt.xlim([0.3, 1.5])
    plt.ylim([0.4e-2, 3e-2])


   

    # Set y-axis to use scientific notation for both major and minor ticks
    ax = plt.gca()
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)   
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    # Change the fontsize of the scientific notation exponent (10^-2)
    ax.yaxis.get_offset_text().set_fontsize(TICK_LABEL_SIZE)  # Adjust this size as needed
    plt.tick_params(axis='y', which='both', labelsize=TICK_LABEL_SIZE)
    plt.savefig(f'{save_path}\\gamma_NO.png', dpi=1000, bbox_inches='tight')
    plt.show()

def plot_gamma_ON(results_list, pressures, y_label='Recombination coefficient'):
    plt.figure(figsize=(8, 6))
    
    for i, results in enumerate(results_list):
        inverse_T = 1000 / results['T']
        plt.semilogy(inverse_T, results['gamma_ON'], label=f'P={pressures[i]} Pa')
    
    apply_plot_formatting(xlabel1, y_label)
    plt.xlim([0.3, 1])
    plt.ylim([4e-4, 4e-3])
    
    # Set y-axis to use scientific notation for both major and minor ticks
    ax = plt.gca()
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)   
    # Set y-axis tick format to 1.0 instead of 1.00
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    # Change the fontsize of the scientific notation exponent (10^-2)
    ax.yaxis.get_offset_text().set_fontsize(TICK_LABEL_SIZE)  # Adjust this size as needed
    plt.tick_params(axis='y', which='both', labelsize=TICK_LABEL_SIZE)
    
    plt.savefig(f'{save_path}\\gamma_ON.png', dpi=1000, bbox_inches='tight')
    plt.show()


# Constants
kB = 1.380649e-23  # Boltzmann constant (m^2 kg)/(s^2 K)
Na = 6.02e+23  # Avogadro constant
h = 6.62607015e-34  # Planck constant

# Parameters
ptot = 1100
p = ptot  # total pressure Pa

C0 = 10 / 11   # O's mole fraction
CN = 1 / 11   # N's mole fraction

s_O = 0.05  # sticking coefficient of species O
s_N = 0.015  # assuming similar sticking coefficient for species N

cA = 3.5  # for thermal desorption

nsite = 5e+18  # site number, /m^2

AA = 0.8
E_OH = 2.5e+3

P_erOO = 0.1
P_erNN = 0.1
P_erON = 0.1
P_erNO = 0.1

Q_erOO = 2.0e+4 / Na  # J/molecule
Q_erNN = 2.0e+4 / Na
Q_erNO = 2.0e+4 / Na
Q_erON = 2.0e+4 / Na

delta = 5.0e-10  # mean distance between sites

Qa_O = 4.998e+5 / Na  # J/molecule
Qa_N = 5.308e+5 / Na

D_OO = 2.550e+5 / Na
D_NN = 3.113e+5 / Na
D_NO = 6.251e+5 / Na  

Em_O = 1.591e+5 / Na
Em_N = 2.362e+5 / Na

Q_lhOO = max(Em_O, 2.0 * Qa_O - D_OO)
Q_lhNN = max(Em_N, 2.0 * Qa_N - D_NN)
Q_lhNO = Qa_O + Qa_N - D_NO

M_O = 16.0   # O's relative atomic mass 
M_N = 14.0  # N's relative atomic mass

mass_O = M_O / 1000 / Na
mass_N = M_N / 1000 / Na
import math

def mass_fraction_to_mole_fraction(components):
    """
    Convert mass fractions to mole fractions.
    :param components: List of dictionaries with component properties: {'fraction': , 'R': , 'gamma': , 'M': }
    :return: List of components with mole fractions.
    """
    denominator = sum(comp['fraction'] / comp['M'] for comp in components)
    for comp in components:
        comp['mole_fraction'] = (comp['fraction'] / comp['M']) / denominator
    return components


def calculate_mixture_properties(components):
    """
    Calculate the gas constant and adiabatic index for a mixture.
    :param components: List of dictionaries with component properties: {'mole_fraction': , 'R': , 'gamma': }
    :return: (R_mix, gamma_mix)
    """
    # Calculate the gas constant for the mixture
    R_mix = sum(comp['mole_fraction'] * comp['R'] for comp in components)

    # Calculate the adiabatic index for the mixture
    gamma_mix = sum(comp['mole_fraction'] * (comp['gamma'] - 1) * comp['R'] for comp in components) / R_mix + 1

    return R_mix, gamma_mix


def calculate_speed_of_sound_mixture(temperature_kelvin, R_mix, gamma_mix):
    # Calculate the speed of sound for the mixture
    speed_of_sound = math.sqrt(gamma_mix * R_mix * temperature_kelvin)
    return speed_of_sound


def calculate_mach_number_mixture(object_speed, temperature_kelvin, R_mix, gamma_mix):
    # Calculate the speed of sound at the given temperature
    speed_of_sound = calculate_speed_of_sound_mixture(temperature_kelvin, R_mix, gamma_mix)

    # Calculate the Mach number
    mach_number = object_speed / speed_of_sound

    return mach_number


# Define properties of components in the mixture based on the provided mass fractions
components = [
    {'name': 'Oxygen gas (O2)', 'fraction': 9.09e-2, 'R': 259.8, 'gamma': 1.4, 'M': 0.032},
    # Oxygen gas (O2), M = 32 g/mol
    {'name': 'Nitrogen gas (N2)', 'fraction': 0.726, 'R': 297.6, 'gamma': 1.4, 'M': 0.028},
    # Nitrogen gas (N2), M = 28 g/mol
    {'name': 'Oxygen atom (O)', 'fraction': 0.131, 'R': 519.6, 'gamma': 1.67, 'M': 0.016},
    # Oxygen atom (O), M = 16 g/mol
    {'name': 'Nitrogen (N)', 'fraction': 4.67e-2, 'R': 593.9, 'gamma': 1.4, 'M': 0.014},  # Nitrogen (N), M = 14 g/mol
    {'name': 'Nitric oxide (NO)', 'fraction': 5.41e-3, 'R': 277.1, 'gamma': 1.4, 'M': 0.030},
    # Nitric oxide (NO), M = 30 g/mol
]

# Convert mass fractions to mole fractions
components = mass_fraction_to_mole_fraction(components)

# Calculate mixture properties
R_mix, gamma_mix = calculate_mixture_properties(components)

# Example: Calculate the Mach number at XX Kelvin for an object traveling at xx m/s
temperature_kelvin = 300
object_speed = 2984  # speed of the object in m/s
mach_number = calculate_mach_number_mixture(object_speed, temperature_kelvin, R_mix, gamma_mix)
print(
    f"At {temperature_kelvin} Kelvin, an object traveling at {object_speed} m/s in the mixture has a Mach number of {mach_number:.2f}")

# Output components with their calculated mole fractions for verification
for comp in components:
    print(f"{comp['name']} - Mass Fraction: {comp['fraction']}, Mole Fraction: {comp['mole_fraction']}")

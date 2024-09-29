def ev_to_jmol(ev_value):
    # constant
    ev_to_j = 1.60218e-19  # eV to J conversion factor
    avogadro_number = 6.022e23  # Avogadro's number
    
    # eV to J/mol conversion
    jmol_value = ev_value * ev_to_j * avogadro_number
    return jmol_value

ev_value = 0.2  # eV value
jmol_value = ev_to_jmol(ev_value)
print(f"{ev_value} eV = {jmol_value:.2f} J/mol")
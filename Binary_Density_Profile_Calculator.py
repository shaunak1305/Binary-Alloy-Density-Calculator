import matplotlib.pyplot as plt
import math

print("--- Advanced Binary Alloy Density Profiler ---")

# 1. Structure
crystal_structure = input("Enter the shared crystal structure (FCC or BCC): ").upper()

if crystal_structure == "FCC":
    atoms_per_cell = 4
elif crystal_structure == "BCC":
    atoms_per_cell = 2
else:
    print("Error: Structure not recognized. Defaulting to 1 atom per cell.")
    atoms_per_cell = 1

# 2. Element A properties
elem_A_name = input("Enter the name of Element A (e.g., Cu): ")
elem_A_wt = float(input(f"Enter atomic weight of {elem_A_name} (g/mol): "))
elem_A_a = float(input(f"Enter lattice parameter of {elem_A_name} in cm (e.g., 3.61e-8): "))

# 3. Element B properties
elem_B_name = input("Enter the name of Element B (e.g., Ni): ")
elem_B_wt = float(input(f"Enter atomic weight of {elem_B_name} (g/mol): "))
elem_B_a = float(input(f"Enter lattice parameter of {elem_B_name} in cm: "))

# --- COMPLEXITY 1: THE BOWING PARAMETER ---
print("\n--- Non-Ideal Solid Solution Parameters ---")
print("Vegard's Law assumes a perfect linear relationship. Real alloys deviate.")
print("A positive bowing parameter expands the lattice. A negative one contracts it.")
b_param = float(input("Enter the empirical bowing parameter 'b' (type 0 for an ideal solution, or try 0.1e-8): "))

# --- COMPLEXITY 2: TEMPERATURE DEPENDENCE ---
print("\n--- Temperature Dependence (Thermal Expansion) ---")
print("Metals expand when heated, increasing lattice volume and decreasing density.")
elem_A_alpha = float(input(f"Enter linear thermal expansion coeff (\u03B1) of {elem_A_name} in 1/°C (e.g., 16.5e-6 for Cu): "))
elem_B_alpha = float(input(f"Enter linear thermal expansion coeff (\u03B1) of {elem_B_name} in 1/°C (e.g., 13.3e-6 for Ni): "))
target_temp = float(input("Enter the target operating temperature in °C (e.g., 1000): "))
base_temp = 20.0  # Standard room temperature assumption
delta_T = target_temp - base_temp

# --- COMPLEXITY 3: POINT DEFECTS (VACANCIES) ---
print("\n--- Defect Modeling (Equilibrium Vacancies) ---")
print("At high temperatures, atoms leave their lattice sites, leaving empty 'vacancies'.")
print("This reduces the effective number of atoms per unit cell, further dropping density.")
elem_A_Qv = float(input(f"Enter vacancy formation energy (Qv) for {elem_A_name} in eV/atom (e.g., 0.9 for Cu): "))
elem_B_Qv = float(input(f"Enter vacancy formation energy (Qv) for {elem_B_name} in eV/atom (e.g., 1.4 for Ni): "))

# 4. Data Storage
compositions_A = []
ideal_densities = []
real_densities = []  
high_temp_densities = []  # List for target temperature densities
defect_densities = []     # List for densities including vacancies

avogadro_number = 6.022e23
k_B = 8.617e-5  # Boltzmann constant in eV/K
target_temp_K = target_temp + 273.15  # Convert to Kelvin for thermodynamics

print("\nCalculating ideal vs. real vs. high-temp vs. defect profiles... Please wait.")

for pct_A in range(0, 101):
    fraction_A = pct_A / 100.0
    fraction_B = 1.0 - fraction_A 

    # Atomic weight follows a linear rule of mixtures
    alloy_weight = (fraction_A * elem_A_wt) + (fraction_B * elem_B_wt)
    
    # --- MATH: Ideal vs. Real Lattice @ 20°C ---
    lattice_ideal = (fraction_A * elem_A_a) + (fraction_B * elem_B_a)
    lattice_real = lattice_ideal + (b_param * fraction_A * fraction_B)

    vol_ideal = lattice_ideal ** 3
    vol_real = lattice_real ** 3
    
    density_ideal = (atoms_per_cell * alloy_weight) / (vol_ideal * avogadro_number)
    density_real = (atoms_per_cell * alloy_weight) / (vol_real * avogadro_number)

    # --- NEW MATH: THERMAL EXPANSION ---
    # 1. Rule of mixtures for the alloy's thermal expansion coefficient
    alloy_alpha = (fraction_A * elem_A_alpha) + (fraction_B * elem_B_alpha)
    
    # 2. Calculate the expanded 1D lattice at the target temperature
    lattice_real_T = lattice_real * (1.0 + (alloy_alpha * delta_T))
    
    # 3. True 3D volumetric expansion is handled automatically by cubing the expanded 1D lattice
    # (a * expansion_factor)^3 inherently scales all three dimensions (x, y, z)
    vol_real_T = lattice_real_T ** 3
    density_real_T = (atoms_per_cell * alloy_weight) / (vol_real_T * avogadro_number)

    # --- NEW MATH: VACANCY DEFECTS ---
    # 1. Rule of mixtures for vacancy formation energy
    alloy_Qv = (fraction_A * elem_A_Qv) + (fraction_B * elem_B_Qv)
    
    # 2. Calculate equilibrium vacancy fraction (Arrhenius equation)
    # X_v = exp(-Qv / kT)
    X_v = math.exp(-alloy_Qv / (k_B * target_temp_K))
    
    # 3. Calculate effective atoms per cell
    effective_atoms_per_cell = atoms_per_cell * (1.0 - X_v)
    
    # 4. Calculate final density with BOTH thermal expansion and vacancies
    density_defect = (effective_atoms_per_cell * alloy_weight) / (vol_real_T * avogadro_number)

    # Store data
    compositions_A.append(pct_A)
    ideal_densities.append(density_ideal)
    real_densities.append(density_real)
    high_temp_densities.append(density_real_T)
    defect_densities.append(density_defect)

# 5. Advanced Graphing
plt.figure(figsize=(10, 7))

# Plot all curves
plt.plot(compositions_A, ideal_densities, color='blue', linestyle='--', linewidth=2, label="Ideal (Vegard's Law) @ 20°C")
plt.plot(compositions_A, real_densities, color='red', linestyle='-', linewidth=2, label=f"Real (b = {b_param}) @ 20°C")
plt.plot(compositions_A, high_temp_densities, color='green', linestyle='-.', linewidth=2, label=f"Real @ {target_temp}°C (Expansion Only)")
plt.plot(compositions_A, defect_densities, color='purple', linestyle=':', linewidth=3, label=f"Real @ {target_temp}°C (Expansion + Vacancies)")

# Labels and title
plt.title(f"Density Profile of {elem_A_name}-{elem_B_name}: Interactions, Expansion & Defects")
plt.xlabel(f"Atomic Percentage of {elem_A_name} (%)")
plt.ylabel("Theoretical Density (g/cm³)")

# Add the legend
plt.legend()
plt.grid(True, alpha=0.5)

plt.show()
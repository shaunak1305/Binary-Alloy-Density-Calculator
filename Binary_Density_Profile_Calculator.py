import matplotlib.pyplot as plt
import math
import csv

def get_valid_float(prompt_text):
    """Continues asking the user until a valid number is entered."""
    while True:
        try:
            # Try to get the input and convert it to a float
            user_input = input(prompt_text)
            return float(user_input)
        except ValueError:
            # If it fails (e.g., typing "3.25r-8"), catch the error and warn the user
            print("   ⚠️ Error: Invalid input! Please enter a valid number.\n")

print("--- Alloy Density Profiler ---")

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
elem_A_wt = get_valid_float(f"Enter atomic weight of {elem_A_name} (g/mol): ")
elem_A_a = get_valid_float(f"Enter lattice parameter of {elem_A_name} in cm (e.g., 3.61e-8): ")

# 3. Element B properties
elem_B_name = input("Enter the name of Element B (e.g., Ni): ")
elem_B_wt = get_valid_float(f"Enter atomic weight of {elem_B_name} (g/mol): ")
elem_B_a = get_valid_float(f"Enter lattice parameter of {elem_B_name} in cm: ")

# --- COMPLEXITY 1: THE BOWING PARAMETER ---
print("\n--- Non-Ideal Solid Solution Parameters ---")
print("Vegard's Law assumes a perfect linear relationship. Real alloys deviate.")
print("A positive bowing parameter expands the lattice. A negative one contracts it.")
b_param = get_valid_float("Enter the empirical bowing parameter 'b' (type 0 for an ideal solution, or try 0.1e-8): ")

# --- COMPLEXITY 2: get_valid_floatTEMPERATURE DEPENDENCE ---
print("\n--- Temperature Dependence (Thermal Expansion) ---")
print("Metals expand when heated, increasing lattice volume and decreasing density.")
elem_A_alpha = get_valid_float(f"Enter linear thermal expansion coeff (\u03B1) of {elem_A_name} in 1/°C (e.g., 16.5e-6 for Cu): ")
elem_B_alpha = get_valid_float(f"Enter linear thermal expansion coeff (\u03B1) of {elem_B_name} in 1/°C (e.g., 13.3e-6 for Ni): ")
target_temp = get_valid_float("Enter the target operating temperature in °C (e.g., 1000): ")
base_temp = get_valid_float("Enter the assumed room temperature in °C (e.g., 25): ")
delta_T = target_temp - base_temp

# --- COMPLEXITY 3: POINT DEFECTS (VACANCIES) ---
print("\n--- Defect Modeling (Equilibrium Vacancies) ---")
print("At high temperatures, atoms leave their lattice sites, leaving empty 'vacancies'.")
print("This reduces the effective number of atoms per unit cell, further dropping density.")
elem_A_Qv = get_valid_float(f"Enter vacancy formation energy (Qv) for {elem_A_name} in eV/atom (e.g., 0.9 for Cu): ")
elem_B_Qv = get_valid_float(f"Enter vacancy formation energy (Qv) for {elem_B_name} in eV/atom (e.g., 1.4 for Ni): ")

# 4. Data Storage
compositions_A = []
ideal_densities = []
real_densities = []  
high_temp_densities = []  # List for target temperature densities
defect_densities = [] #List for room temperature densities
defect_densities_hightemp = []     # List for densities including vacancies

avogadro_number = 6.022e23
k_B = 8.617e-5  # Boltzmann constant in eV/K
room_temp_K = base_temp + 273.15 
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

    # --- MATH: THERMAL EXPANSION ---
    # 1. Rule of mixtures for the alloy's thermal expansion coefficient
    alloy_alpha = (fraction_A * elem_A_alpha) + (fraction_B * elem_B_alpha)
    
    # 2. Calculate the expanded 1D lattice at the target temperature
    lattice_real_T = lattice_real * (1.0 + (alloy_alpha * delta_T))
    
    # 3. True 3D volumetric expansion is handled automatically by cubing the expanded 1D lattice
    vol_real_T = lattice_real_T ** 3
    density_real_T = (atoms_per_cell * alloy_weight) / (vol_real_T * avogadro_number)

    # --- MATH: VACANCY DEFECTS ---
    # 1. Rule of mixtures for vacancy formation energy
    alloy_Qv = (fraction_A * elem_A_Qv) + (fraction_B * elem_B_Qv)
    
    # 2. Calculate equilibrium vacancy fraction (Arrhenius equation)
    # X_v = exp(-Qv / kT)
    X_v_room = math.exp(-alloy_Qv / (k_B * room_temp_K))
    X_v = math.exp(-alloy_Qv / (k_B * target_temp_K))
    
    # 3. Calculate effective atoms per cell
    effective_atoms_per_cell_room = atoms_per_cell * (1.0 - X_v_room)
    effective_atoms_per_cell = atoms_per_cell * (1.0 - X_v)

    
    # 4. Calculate final density with BOTH thermal expansion and vacancies
    density_defect_room = (effective_atoms_per_cell_room * alloy_weight) / (vol_real * avogadro_number)
    density_defect = (effective_atoms_per_cell * alloy_weight) / (vol_real_T * avogadro_number)

    # Store data
    compositions_A.append(pct_A)
    ideal_densities.append(density_ideal)
    real_densities.append(density_real)
    high_temp_densities.append(density_real_T)
    defect_densities.append(density_defect_room)
    defect_densities_hightemp.append(density_defect)

# --- NEW: CSV Data Export ---
print("\n--- Exporting Data ---")
csv_filename = f"{elem_A_name}_{elem_B_name}_density_profile.csv"

try:
    # Open a new file in 'w' (write) mode
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # 1. Write the header row so our Excel columns have titles
        writer.writerow([f"Atomic_Percent_{elem_A_name}", "Ideal_Density_20C", "Real_Density_20C", f"Real_Density_{target_temp}C", "Defect_Density"])
        
        # 2. Loop through our lists and write the data row by row
        for i in range(len(compositions_A)):
            writer.writerow([
                compositions_A[i],
                f"{ideal_densities[i]:.4f}",
                f"{real_densities[i]:.4f}",
                f"{high_temp_densities[i]:.4f}",
                f"{defect_densities[i]:.4f}"
            ])
    print(f"✅ Success! Data successfully exported to {csv_filename}")
except Exception as e:
    print(f"❌ Error saving CSV file: {e}")

# 5. Advanced Graphing
plt.figure(figsize=(10, 7))

# Plot all curves
plt.plot(compositions_A, ideal_densities, color='blue', linestyle='--', linewidth=2, label=f"(Ideal (Vegard's Law) @ {base_temp}")
plt.plot(compositions_A, real_densities, color='red', linestyle='-', linewidth=2, label=f"Real (b = {b_param}) @ {base_temp}")
plt.plot(compositions_A, high_temp_densities, color='green', linestyle='-.', linewidth=2, label=f"Real @ {target_temp}°C (Expansion Only)")
plt.plot(compositions_A, defect_densities_hightemp, color='yellow', linestyle=':', linewidth=3, label=f"Real @ {target_temp}°C (Expansion + Vacancies)")
plt.plot(compositions_A, real_densities, color='orange', linestyle='--', linewidth=2, label=f"Real (b = {b_param}) @ {base_temp} & (Vacancies)")

# Labels and title
plt.title(f"Density Profile of {elem_A_name}-{elem_B_name}: Interactions, Expansion & Defects")
plt.xlabel(f"Atomic Percentage of {elem_A_name} (%)")
plt.ylabel("Theoretical Density (g/cm³)")

# Add the legend
plt.legend()
plt.grid(True, alpha=0.5)

plt.show()

# Binary Alloy Density Profile Calculator

**Overview**

Welcome to my first computational materials science project! This repository contains a Python-based physical metallurgy tool designed to predict and visualize the theoretical density of binary solid solutions across a full compositional range (0% to 100%).

Moving beyond basic textbook idealizations, this computational model layers several real-world thermodynamic and crystallographic phenomena to provide a highly accurate representation of an alloy's density at different temperatures.

**Features & Physics Modeled**

This script calculates material properties by integrating the following concepts:

- Ideal Solid Solutions (Vegard's Law): Calculates the baseline lattice parameter based on a linear rule of mixtures.

- Lattice Distortion (Bowing Parameter): Accounts for atomic size mismatch and electronegativity differences by applying an empirical bowing parameter ($b$) to calculate the non-ideal, "real" lattice parameter.

- Macroscopic Thermodynamics (Thermal Expansion): Applies the Coefficient of Linear Thermal Expansion ($\alpha$) to calculate the 3D volumetric expansion of the unit cell at elevated target temperatures.

- Microscopic Thermodynamics (Point Defects): Utilizes the Arrhenius equation to predict the equilibrium fraction of lattice vacancies at high temperatures, effectively reducing the number of atoms per unit cell.

- Data Visualization: Automatically generates a multi-line plot comparing these physical models using matplotlib.

**Governing Equations**

The model utilizes the following core materials science equations:

- Real Lattice Parameter: 

$$a_{real} = (x_A \cdot a_A + x_B \cdot a_B) + b(x_A \cdot x_B)$$

- Thermal Expansion: 

$$a_T = a_0 \times (1 + \alpha_{alloy} \times \Delta T)$$

- Equilibrium Vacancy Fraction: 

$$X_v = \exp\left(\frac{-Q_v}{k_B \cdot T}\right)$$

- Theoretical Density: 

$$\rho = \frac{n_{effective} \cdot W_{alloy}}{V_c \cdot N_A}$$

(Where $x$ is atomic fraction, $b$ is the bowing parameter, $Q_v$ is vacancy formation energy, and $k_B$ is the Boltzmann constant).

**Installation & Usage**

Prerequisites

You will need Python installed on your machine, along with the matplotlib library for graphing.

**Error Handling**

The project takes care of the error handling in the program by using a function which detects whether the prompt given by the user is correct and creates a loop of asking input till the correct input is obtained from the user.

**CSV Database**

The project will create a CSV database which contains the data points used to plot the final graph.

# About This Project

I created this project as my first foray into Python programming. My goal is to continue building a strong foundation in Computational Materials Science, translating physical metallurgy concepts into robust software tools.

Feel free to explore the code, suggest improvements, or fork the repository!

<img width="1102" height="803" alt="image" src="https://github.com/user-attachments/assets/47767c83-ccf4-4292-8dd7-4dec7caf63e9" />



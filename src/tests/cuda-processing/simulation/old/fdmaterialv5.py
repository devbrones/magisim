import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

# Constants
c = 3e8  # Speed of light in m/s
frequency = 1e9  # Frequency of the source in Hz
wavelength = c / frequency  # Wavelength in meters
dx = dy = wavelength / 10  # Spatial resolution in meters
dt = dx / (2 * c) * 200  # Temporal resolution in seconds

# Grid dimensions and time steps
nx = 200  # Number of grid points in x direction
ny = 200  # Number of grid points in y direction
nt = 5000  # Number of time steps (increased for more iterations)

# Calculate Mur ABC coefficients
dtdx = dt / dx
dtdy = dt / dy
dtdx_2 = dtdx ** 2
dtdy_2 = dtdy ** 2

c_0 = (2 * dtdx - 1) / (2 * dtdx + 1)
c_1 = 2 / (2 * dtdx + 1)
c_2 = (2 * dtdy - 1) / (2 * dtdy + 1)

# Material properties
permittivity_free_space = 8.854187817e-12  # Permittivity of free space in F/m

# Create permittivity arrays for free space
permittivity = permittivity_free_space * np.ones((nx, ny), dtype=complex)  # Permittivity array

# Source parameters
source_position = (50, 50)  # Position of the source (center of the grid)
source_amplitude_dBm = 0.93  # Source amplitude in dBm
source_amplitude_watts = 1e-3 * 10**(source_amplitude_dBm / 10)  # Convert dBm to watts

# Create the grid
grid = np.zeros((nx, ny), dtype=float)

# Set the material properties
material_size = (50, 50)  # Size of the material array
material_position = (75, 75)  # Position of the top-left corner of the material array
material = np.zeros((nx, ny), dtype=bool)
material[material_position[0]:material_position[0] + material_size[0], 
         material_position[1]:material_position[1] + material_size[1]] = True
material_permittivity = 4.0  # Permittivity of the material

# Create a Gaussian source
def gaussian_source(t, t0, sigma):
    return source_amplitude_watts * np.exp(-(t - t0) ** 2 / (2 * sigma ** 2))

# Initialize fields as complex arrays
Ex = np.zeros((nx, ny), dtype=complex)
Hy = np.zeros((nx, ny), dtype=complex)

# Initialize Ex_n and Ex_n_1
Ex_n = Ex.copy()
Ex_n_1 = Ex.copy()

# Create the "animation" directory if it doesn't exist
if not os.path.exists('animation'):
    os.makedirs('animation')

# Simulation loop
for t in tqdm(range(nt), desc="Simulating"):
    # Update magnetic field
    for i in range(1, nx):
        for j in range(1, ny):
            Hy[i, j] = Hy[i, j] + (Ex[i, j] - Ex[i - 1, j]) * dt / dx

    # Update electric field
    for i in range(nx - 1):
        for j in range(ny - 1):
            if material[i, j]:
                Ex[i, j] = Ex[i, j] + (Hy[i, j] - Hy[i, j - 1]) * dt / dx / (permittivity[i, j] * material_permittivity)
            else:
                Ex[i, j] = Ex[i, j] + (Hy[i, j] - Hy[i, j - 1]) * dt / dx / permittivity[i, j]

    # Add the source
    Ex[source_position] += gaussian_source(t, 20, 10 * dt)

    # Mur ABC for top boundary (similar to the original code)
    Ex[0, :] = c_0 * (Ex[2, :] + Ex_n_1[0, :]) + \
              c_1 * (Ex_n[0, :] + Ex_n[2, :] - Ex[1, :] - Ex_n_1[1, :]) + \
              c_2 * Ex_n[1, :] - Ex_n_1[2, :]

    # Mur ABC for bottom boundary (similar to the original code)
    Ex[-1, :] = c_0 * (Ex[-3, :] + Ex_n_1[-1, :]) + \
               c_1 * (Ex_n[-1, :] + Ex_n[-3, :] - Ex[-2, :] - Ex_n_1[-2, :]) + \
               c_2 * Ex_n[-2, :] - Ex_n_1[-3, :]

    # Mur ABC for left boundary (similar to the original code)
    Ex[:, 0] = c_0 * (Ex[:, 2] + Ex_n_1[:, 0]) + \
              c_1 * (Ex_n[:, 0] + Ex_n[:, 2] - Ex[:, 1] - Ex_n_1[:, 1]) + \
              c_2 * Ex_n[:, 1] - Ex_n_1[:, 2]

    # Mur ABC for right boundary (similar to the original code)
    Ex[:, -1] = c_0 * (Ex[:, -3] + Ex_n_1[:, -1]) + \
               c_1 * (Ex_n[:, -1] + Ex_n[:, -3] - Ex[:, -2] - Ex_n_1[:, -2]) + \
               c_2 * Ex_n[:, -2] - Ex_n_1[:, -3]

    # Store previous time step values for ABC
    Ex_n_1 = Ex_n.copy()
    Ex_n = Ex.copy()

    # Save each frame as a PNG image
    if t % 50 == 0:
        plt.figure(figsize=(8, 6))
        plt.imshow(np.abs(Ex.transpose()), cmap='coolwarm', extent=[0, nx * dx, 0, ny * dy])
        plt.colorbar()

        # Display the material region as light gray
        plt.imshow(material.transpose(), cmap='gray', alpha=0.2, extent=[0, nx * dx, 0, ny * dy])
        
        plt.title(f"Field at Time Step {t}")
        plt.xlabel("X (meters)")
        plt.ylabel("Y (meters)")
        plt.savefig(f'animation/frame_{t // 50:04d}.png', dpi=100)
        plt.close()
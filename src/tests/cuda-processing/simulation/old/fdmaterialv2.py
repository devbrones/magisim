import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

# Constants
c = 3e8  # Speed of light in m/s
frequency = 1e9  # Frequency of the source in Hz
wavelength = c / frequency  # Wavelength in meters
dx = dy = wavelength / 10  # Spatial resolution in meters
dt = dx / (2 * c)  # Temporal resolution in seconds

# Grid dimensions and time steps
nx = 200  # Number of grid points in x direction
ny = 200  # Number of grid points in y direction
nt = 5000  # Number of time steps (increased for more iterations)


# Material properties
permittivity_free_space = 8.854187817e-12  # Permittivity of free space in F/m
mx = 50
my = 50



# Create permittivity arrays for free space
permittivity = permittivity_free_space * np.ones((nx, ny))  # Permittivity array

# Source parameters
source_position = (50, 50)  # Position of the source (center of the grid)
source_amplitude_dBm = 0.0  # Source amplitude in dBm
source_amplitude_watts = 1e-3 * 10**(source_amplitude_dBm / 10)  # Convert dBm to watts

# Create the grid
grid = np.zeros((nx, ny), dtype=float)
material = np.full((mx, my), fill_value=True, dtype=bool)

# Set the material properties
csx, csy = 100, 100  # Coordinates of the center of the material
material[csx, csy] = True
material_permittivity = 4.0  # Permittivity of the material

# Create a Gaussian source
def gaussian_source(t, t0, sigma):
    return source_amplitude_watts * np.exp(-(t - t0) ** 2 / (2 * sigma ** 2))

# Create a directory to store animation frames
if not os.path.exists('animation'):
    os.makedirs('animation')

# Initialize fields
Ex = np.zeros((nx, ny), dtype=float)
Hy = np.zeros((nx, ny), dtype=float)

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

    # Save each frame as a PNG image
    if t % 50 == 0:
        plt.figure(figsize=(8, 6))
        plt.imshow(Ex.transpose(), cmap='coolwarm', extent=[0, nx * dx, 0, ny * dy])
        plt.colorbar()
        plt.title(f"Field at Time Step {t}")
        plt.xlabel("X (meters)")
        plt.ylabel("Y (meters)")
        plt.savefig(f'animation/frame_{t // 50:04d}.png', dpi=100)
        plt.close()

# To convert the frames into an animation, you can use software like ffmpeg or image processing libraries.

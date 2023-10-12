import numpy as np
import numba
from numba import cuda
import cmath
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define constants for Mur ABC
@numba.jit
def calculate_mur_coefficients(dt, dx, dy):
    dtdx = cmath.sqrt(dt / dx * dt / dy)
    dtdx_2 = 1 / dtdx + 2 + dtdx
    c_0 = -(1 / dtdx - 2 + dtdx) / dtdx_2
    c_1 = -2 * (dtdx - 1 / dtdx) / dtdx_2
    c_2 = 4 * (dtdx + 1 / dtdx) / dtdx_2
    return c_0, c_1, c_2

# Update magnetic fields at time step n+1/2
@cuda.jit
def update_magnetic_fields(H_x, H_y, E_z_real, dt, dx, dy):
    i, j = cuda.grid(2)
    if 0 < i < Nx and 0 <= j < Ny - 1:
        H_x[i, j] -= dt / dy * (E_z_real[i, j + 1] - E_z_real[i, j])
    if 0 <= i < Nx - 1 and 0 <= j < Ny:
        H_y[i, j] += dt / dx * (E_z_real[i + 1, j] - E_z_real[i, j])

# Update electric field at time step n+1
@cuda.jit
def update_electric_field(E_z_real, E_z_imag, H_x, H_y, dt, dx, dy):
    i, j = cuda.grid(2)
    if 1 <= i < Nx - 1 and 1 <= j < Ny - 1:
        diff_H_x = dt / dy * (H_x[i, j] - H_x[i, j - 1])
        diff_H_y = dt / dx * (H_y[i, j] - H_y[i - 1, j])
        E_z_real[i, j] += diff_H_y - diff_H_x
        E_z_imag[i, j] += diff_H_y - diff_H_x

# Apply Mur ABC for boundaries
@cuda.jit
def apply_mur_boundary(E_z, c_0, c_1, c_2):
    i, j = cuda.grid(2)
    if i == 0:
        E_z[i, j] = c_0 * (E_z[i + 2, j] + E_z[i, j]) + \
                    c_1 * (E_z[i + 1, j] + E_z[i + 2, j] - E_z[i + 1, j] - E_z[i, j]) + \
                    c_2 * E_z[i + 1, j] - E_z[i, j]
    if i == Nx - 1:
        E_z[i, j] = c_0 * (E_z[i - 2, j] + E_z[i, j]) + \
                    c_1 * (E_z[i - 1, j] + E_z[i - 2, j] - E_z[i - 1, j] - E_z[i, j]) + \
                    c_2 * E_z[i - 1, j] - E_z[i, j]
    if j == 0:
        E_z[i, j] = c_0 * (E_z[i, j + 2] + E_z[i, j]) + \
                    c_1 * (E_z[i, j + 1] + E_z[i, j + 2] - E_z[i, j + 1] - E_z[i, j]) + \
                    c_2 * E_z[i, j + 1] - E_z[i, j]
    if j == Ny - 1:
        E_z[i, j] = c_0 * (E_z[i, j - 2] + E_z[i, j]) + \
                    c_1 * (E_z[i, j - 1] + E_z[i, j - 2] - E_z[i, j - 1] - E_z[i, j]) + \
                    c_2 * E_z[i, j - 1] - E_z[i, j]

# Initialize and run the FDTD simulation
def run_fdtd_simulation(Nx, Ny, c, dx, dy, n_iter):
    # Initialize complex electric field
    E_z_real = cuda.device_array((Nx, Ny))
    E_z_imag = cuda.device_array((Nx, Ny))

    # Initialize arrays for H_x and H_y
    H_x = cuda.device_array((Nx, Ny - 1))
    H_y = cuda.device_array((Nx - 1, Ny))


    # Source location
    source_x = int(Nx / 2)
    source_y = int(Ny / 2)

    # Time parameters
    dt = min(dx, dy) / np.sqrt(2) / c
    tmax = n_iter * dt

    # Grid parameters
    block_dim = (16, 16)
    grid_dim = ((Nx - 1) // block_dim[0] + 1, (Ny - 1) // block_dim[1] + 1)

    # Calculate Mur ABC coefficients
    c_0, c_1, c_2 = calculate_mur_coefficients(dt, dx, dy)

    # Main FDTD loop
    for n in range(n_iter):
        # Update magnetic fields
        update_magnetic_fields[grid_dim, block_dim](H_x, H_y, E_z_real, dt, dx, dy)

        # Update electric field
        update_electric_field[grid_dim, block_dim](E_z_real, E_z_imag, H_x, H_y, dt, dx, dy)

        # Gaussian pulse excitation
        tp = 30
        if n * dt <= tp:
            C = (7 / 3) ** 3 * (7 / 4) ** 4
            pulse = C * (n * dt / tp) ** 3 * (1 - n * dt / tp) ** 4
        else:
            pulse = 0

        # Apply source at the center
        E_z_real[source_x, source_y] += pulse
        E_z_imag[source_x, source_y] += pulse  # Apply the pulse to the imaginary part as well
        
        # Apply Mur ABC for boundaries for both real and imaginary parts
        apply_mur_boundary[grid_dim, block_dim](E_z_real, c_0, c_1, c_2)
        apply_mur_boundary[grid_dim, block_dim](E_z_imag, c_0, c_1, c_2)
        
        # Plot the electric field at certain time steps (optional) for both real and imaginary parts
        if n % 10 == 0:
            plot_field(E_z_real, dx, dy, n * dt)  # Plot the real part
            plot_field(E_z_imag, dx, dy, n * dt)  # Plot the imaginary part


# Function to plot the electric field
def plot_field(E_z, dx, dy, t):
    plt.figure()
    plt.imshow(np.abs(E_z.copy_to_host()), extent=[0, dx * Nx, 0, dy * Ny], cmap='inferno')
    plt.colorbar()
    plt.title(f"Electric Field at t = {t:.2f} s")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.show()

# Simulation parameters
Nx = 200  # Number of grid points in the x-direction
Ny = 200  # Number of grid points in the y-direction
c = 1.0   # Speed of light in vacuum (normalized to 1)
dx = 1e-3  # Spatial resolution in meters
dy = 1e-3  # Spatial resolution in meters
n_iter = 500  # Number of time steps

# Run the FDTD simulation
E_z_result = run_fdtd_simulation(Nx, Ny, c, dx, dy, n_iter)

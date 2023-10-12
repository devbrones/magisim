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

# Initialize and run the FDTD simulation
def run_fdtd_simulation(Nx, Ny, c, dx, dy, n_iter):
    # Initialize arrays for real and imaginary parts of E_z
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

    # Get Mur ABC coefficients
    c_0, c_1, c_2 = calculate_mur_coefficients(dt, dx, dy)

    # CUDA grid and block dimensions
    block_dim = (16, 16)
    grid_dim = ((Nx - 1) // block_dim[0] + 1, (Ny - 1) // block_dim[1] + 1)

    # Run CUDA-accelerated FDTD simulation
    for n in range(n_iter):
        update_magnetic_fields[grid_dim, block_dim](H_x, H_y, E_z_real, dt, dx, dy)
        update_electric_field[grid_dim, block_dim](E_z_real, E_z_imag, H_x, H_y, dt, dx, dy)

        # Pulse at time step n+1
        tp = 30
        if n * dt <= tp:
            C = (7 / 3) ** 3 * (7 / 4) ** 4
            pulse = C * (n * dt / tp) ** 3 * (1 - n * dt / tp) ** 4
        else:
            pulse = 0

        E_z_real[source_x, source_y] += pulse

        # Apply Mur ABC for boundaries
        # Apply Mur ABC for boundaries
        blockspergrid = (Nx, Ny)
        threadsperblock = (16, 16)

        apply_mur_boundary[blockspergrid, threadsperblock](E_z_real, E_z_imag, c_0, c_1, c_2)

    # Copy the results back to the host
    E_z_real_host = E_z_real.copy_to_host()
    E_z_imag_host = E_z_imag.copy_to_host()

    # Combine real and imaginary parts to form the complex field
    E_z_result = E_z_real_host + 1j * E_z_imag_host

    return E_z_result


# Apply Mur ABC for boundaries
@numba.jit
def apply_mur_boundary(E_z_real, E_z_imag, c_0, c_1, c_2):
    Nx, Ny = E_z_real.shape
    for i in range(Nx):
        for j in range(Ny):
            if i == 0:
                E_z_real[i, j] = c_0 * (E_z_real[i + 2, j] + E_z_real[i, j]) + \
                                 c_1 * (E_z_real[i + 1, j] + E_z_real[i + 2, j] - E_z_real[i + 1, j] - E_z_real[i, j]) + \
                                 c_2 * E_z_real[i + 1, j] - E_z_real[i, j]
                E_z_imag[i, j] = c_0 * (E_z_imag[i + 2, j] + E_z_imag[i, j]) + \
                                 c_1 * (E_z_imag[i + 1, j] + E_z_imag[i + 2, j] - E_z_imag[i + 1, j] - E_z_imag[i, j]) + \
                                 c_2 * E_z_imag[i + 1, j] - E_z_imag[i, j]
            if i == Nx - 1:
                E_z_real[i, j] = c_0 * (E_z_real[i - 2, j] + E_z_real[i, j]) + \
                                 c_1 * (E_z_real[i - 1, j] + E_z_real[i - 2, j] - E_z_real[i - 1, j] - E_z_real[i, j]) + \
                                 c_2 * E_z_real[i - 1, j] - E_z_real[i, j]
                E_z_imag[i, j] = c_0 * (E_z_imag[i - 2, j] + E_z_imag[i, j]) + \
                                 c_1 * (E_z_imag[i - 1, j] + E_z_imag[i - 2, j] - E_z_imag[i - 1, j] - E_z_imag[i, j]) + \
                                 c_2 * E_z_imag[i - 1, j] - E_z_imag[i, j]
            if j == 0:
                E_z_real[i, j] = c_0 * (E_z_real[i, j + 2] + E_z_real[i, j]) + \
                                 c_1 * (E_z_real[i, j + 1] + E_z_real[i, j + 2] - E_z_real[i, j + 1] - E_z_real[i, j]) + \
                                 c_2 * E_z_real[i, j + 1] - E_z_real[i, j]
                E_z_imag[i, j] = c_0 * (E_z_imag[i, j + 2] + E_z_imag[i, j]) + \
                                 c_1 * (E_z_imag[i, j + 1] + E_z_imag[i, j + 2] - E_z_imag[i, j + 1] - E_z_imag[i, j]) + \
                                 c_2 * E_z_imag[i, j + 1] - E_z_imag[i, j]
            if j == Ny - 1:
                E_z_real[i, j] = c_0 * (E_z_real[i, j - 2] + E_z_real[i, j]) + \
                                 c_1 * (E_z_real[i, j - 1] + E_z_real[i, j - 2] - E_z_real[i, j - 1] - E_z_real[i, j]) + \
                                 c_2 * E_z_real[i, j - 1] - E_z_real[i, j]
                E_z_imag[i, j] = c_0 * (E_z_imag[i, j - 2] + E_z_imag[i, j]) + \
                                 c_1 * (E_z_imag[i, j - 1] + E_z_imag[i, j - 2] - E_z_imag[i, j - 1] - E_z_imag[i, j]) + \
                                 c_2 * E_z_imag[i, j - 1] - E_z_imag[i, j]
                
    return E_z_real, E_z_imag


# Apply Mur ABC for boundaries
@numba.jit
def apply_mur_boundary(E_z_real, E_z_imag, c_0, c_1, c_2):
    i, j = cuda.grid(2)
    if i == 0:
        E_z_real[i, j] = c_0 * (E_z_real[i + 2, j] + E_z_real[i, j]) + \
                         c_1 * (E_z_real[i + 1, j] + E_z_real[i + 2, j] - E_z_real[i + 1, j] - E_z_real[i, j]) + \
                         c_2 * E_z_real[i + 1, j] - E_z_real[i, j]
        E_z_imag[i, j] = c_0 * (E_z_imag[i + 2, j] + E_z_imag[i, j]) + \
                         c_1 * (E_z_imag[i + 1, j] + E_z_imag[i + 2, j] - E_z_imag[i + 1, j] - E_z_imag[i, j]) + \
                         c_2 * E_z_imag[i + 1, j] - E_z_imag[i, j]
    

# Define simulation parameters
Nx = 101
Ny = 101
c = 1
dx = 1
dy = 1
n_iter = 180

# Run the CUDA-accelerated simulation
E_z_result = run_fdtd_simulation(Nx, Ny, c, dx, dy, n_iter)

# Plot or animate the results as needed
# For example, you can create an animation of the E-field using FuncAnimation
def animate_E(i):
    plt.clf()
    plt.pcolormesh(E_z_result.real.T, shading="auto", cmap="bwr")
    plt.axis("equal")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)

ani = FuncAnimation(plt.figure(), animate_E, frames=n_iter, repeat=False)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import cuda

# Constants
c = 299792458.0  # Speed of light in m/s
epsilon_0 = 8.854187817e-12  # Permittivity of free space in F/m
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space in H/m

# Simulation parameters
grid_size = (200, 200)
dx = dy = 1e-3
dt = dx / (2 * c)
simulation_time = 3.0  # seconds
num_steps = int(simulation_time / dt)

# CUDA kernel
@cuda.jit
def update_e_field(Ez, Hy):
    i, j = cuda.grid(2)
    
    if i < Ez.shape[0] - 1 and j < Ez.shape[1] - 1:
        c1 = dt / epsilon_0 / dx
        c2 = dt / epsilon_0 / dy
        
        # Update Ez field
        if i > 0 and j > 0:
            Ez[i, j] += c1 * (Hy[i, j] - Hy[i - 1, j]) - c2 * (Hy[i, j] - Hy[i, j - 1])

@cuda.jit
def update_h_field(Ez, Hy):
    i, j = cuda.grid(2)
    
    if i < Hy.shape[0] - 1 and j < Hy.shape[1] - 1:
        c3 = dt / mu_0 / dx
        c4 = dt / mu_0 / dy
        
        # Update Hy field
        if i < Ez.shape[0] - 1 and j < Ez.shape[1] - 1:
            Hy[i, j] += c3 * (Ez[i, j + 1] - Ez[i, j]) - c4 * (Ez[i + 1, j] - Ez[i, j])

# Initialize fields
Ez = np.zeros(grid_size, dtype=np.float32)
Hy = np.zeros(grid_size, dtype=np.float32)

# Create a figure for animation
fig = plt.figure()
ims = []

# Main simulation loop
for step in range(num_steps):
    # Update E field using CUDA
    update_e_field[grid_size, 1](Ez, Hy)
    
    # Update H field using CUDA
    update_h_field[grid_size, 1](Ez, Hy)
    
    # Append current Ez field to the animation frames
    im = plt.imshow(Ez, animated=True, cmap='RdBu', vmin=-0.1, vmax=0.1)
    ims.append([im])

# Create the animation
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True)

# Save animation as GIF
ani.save('fdtd_simulation.gif', writer='pillow')

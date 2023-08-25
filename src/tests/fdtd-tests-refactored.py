import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from numba import cuda
from tqdm import tqdm
import os

# Constants
epsilon_0 = 8.854e-12  # F/m (vacuum permittivity)
mu_0 = 4e-7 * np.pi    # H/m (vacuum permeability)
c = 1 / np.sqrt(epsilon_0 * mu_0)  # Speed of light in m/s
air = True  # Whether to simulate in air or vacuum
if air:
    # Permittivity of atmospheric air (F/m)
    epsilon_0 = 1.0006
    # Permeability of atmospheric air (H/m)
    mu_0 = mu_0  # Assume it's the same as vacuum permeability

# Simulation parameters
simulation_time_ns = 10e-9  # Simulation time in nanoseconds
grid_size = (2000, 2000)
dx = dy = 5e-3
dt = dx / (2 * c)  # CFL stability condition for FDTD
num_steps = int(simulation_time_ns / dt)  # Calculate the number of steps based on simulation time

# Allocate GPU arrays for Ez and Hy
Ez_gpu = cuda.device_array(grid_size, dtype=np.float64)
Hy_gpu = cuda.device_array(grid_size, dtype=np.float64)

# Define the update functions as CUDA kernels
@cuda.jit
def update_h_field(Ez, Hy):
    i, j = cuda.grid(2)
    if 0 < i < grid_size[0] - 1 and 0 < j < grid_size[1] - 1:
        Hy[i, j] -= (Ez[i + 1, j] - Ez[i, j]) * dt / (mu_0 * dx)
        Hy[i, j] -= (Ez[i, j + 1] - Ez[i, j]) * dt / (mu_0 * dy)

@cuda.jit
def update_e_field(Ez, Hy):
    i, j = cuda.grid(2)
    if 0 < i < grid_size[0] - 1 and 0 < j < grid_size[1] - 1:
        Ez[i, j] += (Hy[i, j] - Hy[i - 1, j]) * dt * c / dx
        Ez[i, j] += (Hy[i, j] - Hy[i, j - 1]) * dt * c / dy

# Initialize the figure and axis for visualization
fig = plt.figure()
ax = plt.axes()

# Create empty list to store animation frames
ims = []

# Main simulation loop
with tqdm(total=num_steps, desc="Simulation Progress") as pbar:
    for step in range(num_steps):
        # Update H field using CUDA
        update_h_field[grid_size, 1](Ez_gpu, Hy_gpu)
        
        # Source excitation (a simple Gaussian pulse)
        Ez_gpu[grid_size[0] // 2, grid_size[1] // 2] = np.exp(-(0.5 * ((step - 30) / 10) ** 2))
        
        # Update E field using CUDA
        update_e_field[grid_size, 1](Ez_gpu, Hy_gpu)
        
        # Append current Ez field to the animation frames
        im = plt.imshow(Ez_gpu.copy_to_host(), animated=True, cmap='jet', extent=[0, grid_size[1] * dx, 0, grid_size[0] * dy], vmin=-0.1, vmax=0.1)
        ims.append([im])
        
        pbar.update(1)  # Update the progress bar
print("Simulation complete! Saving animation...")

# Create the animation
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True)

# Save animation as MP4
ani.save('fdtd_simulation.mp4', writer='ffmpeg')

# Save individual frames as PNG images
if not os.path.exists("frames"):
    os.makedirs("frames")

for i, im in enumerate(ims):
    frame_filename = f"frames/frame_{i:04d}.png"
    im[0].figure.savefig(frame_filename, format="png")
    plt.close(im[0].figure)

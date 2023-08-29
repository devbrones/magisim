import numpy as np
import matplotlib.pyplot as plt
from numba import cuda
from tqdm import tqdm
import os

# Constants
epsilon_0 = 8.854e-12
mu_0 = 4e-7 * np.pi
c = 1 / np.sqrt(epsilon_0 * mu_0)
air = True
if air:
    epsilon_0 = 1.0006
    mu_0 = mu_0

# Simulation parameters
simulation_time_ns = 50e-9
grid_size = (200, 200)
dx = dy = 5e-3
dt = dx / (2 * (c/2))
num_steps = int(simulation_time_ns / dt)

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


# Main simulation loop
with tqdm(total=num_steps, desc="Simulation Progress") as pbar:
    for step in range(num_steps):

        # Update H field using CUDA
        update_h_field[grid_size, 1](Ez_gpu, Hy_gpu)
        
        # Source excitation (a simple Gaussian pulse)
        Ez_gpu[grid_size[0] // 2, grid_size[1] // 2] = np.exp(-(0.5 * ((step - 30) / 10) ** 2))
        
        # Update E field using CUDA
        update_e_field[grid_size, 1](Ez_gpu, Hy_gpu)
        
        pbar.update(1)

print("Simulation complete! Saving frames...")

# Save individual frames as PNG images
if not os.path.exists("frames"):
    os.makedirs("frames")

frame_folder = "frames"  # Set the folder where frames will be saved
frame_filenames = []  # List to store frame filenames

for step in tqdm(range(num_steps), desc="Saving Frames"):
    plt.imshow(Ez_gpu.copy_to_host(), cmap='jet', extent=[0, grid_size[1] * dx, 0, grid_size[0] * dy], vmin=-0.1, vmax=0.1)
    
    frame_filename = os.path.join(frame_folder, f"frame_{step:04d}.png")
    frame_filenames.append(frame_filename)  # Store the filename
    
    plt.savefig(frame_filename, format="png")
    plt.clf()  # Clear the figure
print("Frames saved.")

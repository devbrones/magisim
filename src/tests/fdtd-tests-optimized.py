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
grid_size = (2000, 2000)
dx = dy = 5e-3
dt = dx / (2 * c)
num_steps = int(simulation_time_ns / dt)

# Allocate a single GPU array for both Ez and Hy
EzHy_gpu = cuda.device_array(grid_size, dtype=np.float32)

# Define the update function as a CUDA kernel
@cuda.jit
def update_fields(EzHy):
    i, j = cuda.grid(2)
    if 0 < i < grid_size[0] - 1 and 0 < j < grid_size[1] - 1:
        EzHy[i, j] += (EzHy[i, j] - EzHy[i - 1, j]) * dt * c / dx
        EzHy[i, j] += (EzHy[i, j] - EzHy[i, j - 1]) * dt * c / dy
        EzHy[i, j] -= (EzHy[i + 1, j] - EzHy[i, j]) * dt / (mu_0 * dx)
        EzHy[i, j] -= (EzHy[i, j + 1] - EzHy[i, j]) * dt / (mu_0 * dy)

# Main simulation loop
with tqdm(total=num_steps, desc="Simulation Progress") as pbar:
    for step in range(num_steps):
        update_fields[grid_size, 1](EzHy_gpu)
        
        # Add a pulse source (Gaussian pulse)
        pulse_center = grid_size[0] // 2
        pulse_duration = 10
        pulse_amplitude = np.exp(-(0.5 * ((step - 30) / pulse_duration) ** 2))
        EzHy_gpu[pulse_center, pulse_center] += pulse_amplitude

        pbar.update(1)
print("Simulation complete! Saving frames...")
# Save individual frames as PNG images
if not os.path.exists("frames"):
    os.makedirs("frames")

for step in tqdm(range(num_steps), desc="Saving Frames"):
    plt.imshow(EzHy_gpu.copy_to_host(), cmap='jet', extent=[0, grid_size[1] * dx, 0, grid_size[0] * dy], vmin=-0.1, vmax=0.1)
    plt.savefig(f"frames/frame_{step:04d}.png", format="png")
    plt.clf()  # Clear the figure

print("Frames saved.")

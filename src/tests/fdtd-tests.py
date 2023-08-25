import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import cuda
import os
from tqdm import tqdm

# Constants and simulation parameters
c = 299792458.0  # Speed of light in m/s
epsilon_0 = 8.854187817e-12  # Permittivity of free space in F/m
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space in H/m
grid_size = (200, 200)
dx = dy = 1e-3
dt = dx / (2 * c)
simulation_time = (1e-9)/1.5  # seconds
num_steps = int(simulation_time / dt)

# Create a directory to store frames
if not os.path.exists("frames"):
    os.makedirs("frames")

# CUDA kernel functions
@cuda.jit
def update_e_field(Ez, Hy):
    i, j = cuda.grid(2)
    
    if i > 0 and j > 0 and i < Ez.shape[0] - 1 and j < Ez.shape[1] - 1:
        c1 = dt / epsilon_0 / dx
        c2 = dt / epsilon_0 / dy
        
        # Update Ez field
        Ez[i, j] += c1 * (Hy[i, j] - Hy[i - 1, j]) - c2 * (Hy[i, j] - Hy[i, j - 1])

@cuda.jit
def update_h_field(Ez, Hy):
    i, j = cuda.grid(2)
    
    if i >= 0 and j >= 0 and i < Hy.shape[0] - 1 and j < Hy.shape[1] - 1:
        c3 = dt / mu_0 / dx
        c4 = dt / mu_0 / dy
        
        # Update Hy field
        Hy[i, j] += c3 * (Ez[i, j + 1] - Ez[i, j]) - c4 * (Ez[i + 1, j] - Ez[i, j])

# Initialize fields
Ez = np.zeros(grid_size, dtype=np.float32)
Hy = np.zeros(grid_size, dtype=np.float32)

# Create a figure for animation
fig = plt.figure()
ims = []
# Allocate GPU arrays for Ez and Hy
Ez_gpu = cuda.to_device(Ez)
Hy_gpu = cuda.to_device(Hy)

# Run simulation
# Main simulation loop without saving individual frames
animation_images = []  # List to store animation images

with tqdm(total=num_steps, desc="Simulation Progress") as pbar:
    for step in range(num_steps):
        # Update H field using CUDA
        update_h_field[grid_size, 1](Ez, Hy)
        
        # Source excitation using the specified Gaussian pulse pattern
        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                distance = np.sqrt((i - grid_size[0] // 2)**2 + (j - grid_size[1] // 2)**2)
                Ez[i, j] = np.exp(-(0.5 * ((step - 30) / 10) ** 2)) * np.exp(-0.1 * distance)
        
        # Update E field using CUDA
        update_e_field[grid_size, 1](Ez, Hy)
        
        # Plot the current Ez field and store the pixel data
        im = plt.imshow(Ez, animated=True, cmap='RdBu', extent=[0, grid_size[1] * dx, 0, grid_size[0] * dy], vmin=-0.1, vmax=0.1)
        animation_images.append(im.get_array())  # Store pixel data
        
        pbar.update(1)  # Update the progress bar

# Create the animation
ani = animation.ArtistAnimation(fig, [], interval=50, blit=True)

# Save animation as MP4
ani.save('fdtd_simulation.mp4', writer='ffmpeg')

# Save individual frames as PNG images
if not os.path.exists("frames"):
    os.makedirs("frames")

for i, im_data in enumerate(animation_images):
    plt.imshow(im_data, cmap='RdBu', extent=[0, grid_size[1] * dx, 0, grid_size[0] * dy], vmin=-0.1, vmax=0.1)
    frame_filename = f"frames/frame_{i:04d}.png"
    plt.savefig(frame_filename, format="png")
    plt.clf()  # Clear the figure to avoid overwriting

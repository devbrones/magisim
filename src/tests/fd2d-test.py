import argparse
import numpy as np
from numba import cuda, float64
import matplotlib.pyplot as plt
from tqdm import tqdm

# Constants
c = 299792458.0  # Speed of light in m/s
euler_number = np.e  # Euler's number

# FDTD simulation kernel
@cuda.jit
def fdtd_simulation_kernel(ez, hx, hy, gaz, t, grid_size, dt, epsilon0):
    i, j = cuda.grid(2)
    
    if i < grid_size - 1 and j < grid_size - 1:
        if j > 0 and i > 0:
            dz = 0.5 * (hy[i, j] - hy[i - 1, j] - hx[i, j] + hx[i, j - 1])
            ez[i, j] = gaz[i, j] * dz
        
        if i > 0 and j > 0 and i < grid_size - 1 and j < grid_size - 1:
            hx[i, j] += 0.5 * (ez[i, j + 1] - ez[i, j])
            hy[i, j] += 0.5 * (ez[i + 1, j] - ez[i, j])
        
        if i == grid_size // 2 and j == grid_size // 2:
            ez[i, j] = euler_number ** (-0.5 * ((t - 30) / 10)**2)  # Exponential calculation using Euler's number

def main(grid_size, sim_time_ns):
    # Parameters
    dt = 0.5e-12  # Reduced dt value
    epsilon0 = 8.854187817e-12

    # Calculate number of time steps
    num_steps = int(sim_time_ns / dt)

    # Initialize arrays on the CPU and GPU
    ez = np.zeros((grid_size, grid_size))
    hx = np.zeros((grid_size, grid_size))
    hy = np.zeros((grid_size, grid_size))
    gaz = np.ones((grid_size, grid_size)) * (dt / epsilon0)
    ez_gpu = cuda.to_device(ez)
    hx_gpu = cuda.to_device(hx)
    hy_gpu = cuda.to_device(hy)
    gaz_gpu = cuda.to_device(gaz)

    # Initialize CUDA grid and block dimensions
    threadsperblock = (16, 16)
    blockspergrid_x = (grid_size + threadsperblock[0] - 1) // threadsperblock[0]
    blockspergrid_y = (grid_size + threadsperblock[1] - 1) // threadsperblock[1]
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    # Run simulation on GPU
    for t in tqdm(range(num_steps), desc="Simulation Progress"):
        fdtd_simulation_kernel[blockspergrid, threadsperblock](ez_gpu, hx_gpu, hy_gpu, gaz_gpu, t, grid_size, dt, epsilon0)

    # Copy the result back to the CPU
    ez_result = ez_gpu.copy_to_host()

    # Save frames as PNG images
    for t in tqdm(range(ez_result.shape[0]), desc="Saving Frames"):
        plt.imshow(ez_result[t], cmap='RdBu', extent=[0, grid_size, 0, grid_size])
        plt.colorbar(label="Electric Field (V/m)")
        plt.title(f"Time Step {t}")
        plt.savefig(f"frame_{t:03d}.png")
        plt.clf()

    print("Simulation completed and frames saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FDTD Simulation with CUDA")
    parser.add_argument("--gridsize", type=int, default=200, help="Grid size")
    parser.add_argument("--simtimens", type=int, default=50e-9, help="Simulation time in nanoseconds")
    args = parser.parse_args()

    main(args.gridsize, args.simtimens)

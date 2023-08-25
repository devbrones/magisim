# fdtd tests for cpu and gpu
import numpy as np
from numba import jit, cuda
import matplotlib.pyplot as plt
import time

# Define simulation parameters
nx = 200
ny = 200
nt = 100

# Define material properties
c = 1.0
dx = 0.01
dy = 0.01
dt = 0.001

# Define source parameters
x0 = 100
y0 = 100
f0 = 50

# Define update equations
@jit
def update_cpu(u, un):
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            un[i, j] = 2 * u[i, j] - un[i, j] + c ** 2 * dt ** 2 / dx ** 2 * (u[i + 1, j] - 2 * u[i, j] + u[i - 1, j]) + c ** 2 * dt ** 2 / dy ** 2 * (u[i, j + 1] - 2 * u[i, j] + u[i, j - 1])
    return un

@cuda.jit
def update_gpu(u, un):
    i, j = cuda.grid(2)
    if 1 <= i < nx - 1 and 1 <= j < ny - 1:
        un[i, j] = 2 * u[i, j] - un[i, j] + c ** 2 * dt ** 2 / dx ** 2 * (u[i + 1, j] - 2 * u[i, j] + u[i - 1, j]) + c ** 2 * dt ** 2 / dy ** 2 * (u[i, j + 1] - 2 * u[i, j] + u[i, j - 1])

# Initialize arrays
u = np.zeros((nx, ny))
un = np.zeros((nx, ny))

# Set up source
x = np.arange(nx)
y = np.arange(ny)
X, Y = np.meshgrid(x, y)
u[x0, y0] = np.exp(-f0 * ((X - x0) ** 2 + (Y - y0) ** 2))

# Run simulation on CPU
start_cpu = time.time()
for n in range(nt):
    un = update_cpu(u, un)
    u, un = un, u
end_cpu = time.time()

# Run simulation on GPU
threadsperblock = (16, 16)
blockspergrid_x = int(np.ceil(nx / threadsperblock[0]))
blockspergrid_y = int(np.ceil(ny / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)

u = np.zeros((nx, ny))
un = np.zeros((nx, ny))
u[x0, y0] = np.exp(-f0 * ((X - x0) ** 2 + (Y - y0) ** 2))

start_gpu = time.time()
for n in range(nt):
    update_gpu[blockspergrid, threadsperblock](u, un)
    u, un = un, u
end_gpu = time.time()

# Print timing results
print("CPU time:", end_cpu - start_cpu)
print("GPU time:", end_gpu - start_gpu)

# Plot results
plt.imshow(u)
plt.show()
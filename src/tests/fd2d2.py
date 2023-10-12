import numpy as np
from math import exp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import cuda
from tqdm import tqdm

# Parameters
ie = 60
je = 60
ic = int(ie / 2)
jc = int(je / 2)
nsteps = 60
t0 = 20
spread = 6
dt = 10

# CUDA setup
threadsperblock = (16, 16)
blockspergrid_x = (ie + threadsperblock[0] - 1) // threadsperblock[0]
blockspergrid_y = (je + threadsperblock[1] - 1) // threadsperblock[1]
blockspergrid = (blockspergrid_x, blockspergrid_y)

# Initialize arrays on host
ez = np.zeros((ie, je), dtype=np.float32)
dz = np.zeros((ie, je), dtype=np.float32)
hx = np.zeros((ie, je), dtype=np.float32)
hy = np.zeros((ie, je), dtype=np.float32)
gaz = np.ones((ie, je), dtype=np.float32)
pulse = np.zeros((ie, je), dtype=np.float32)
pulse[ic, jc] = 1

# Allocate device arrays
ez_d = cuda.to_device(ez)
dz_d = cuda.to_device(dz)
hx_d = cuda.to_device(hx)
hy_d = cuda.to_device(hy)
gaz_d = cuda.to_device(gaz)
pulse_d = cuda.to_device(pulse)

# CUDA kernel
@cuda.jit
def fdtd_cuda(dz, ez, hx, hy, gaz, ic, jc, t0, spread, time_step, pulse):
    i, j = cuda.grid(2)
    
    if 0 < i < ie - 1 and 0 < j < je - 1:
        dz[i, j] = dz[i, j] + 0.5 * (hy[i, j] - hy[i - 1, j] - hx[i, j] + hx[i, j - 1])
        
        if time_step == 1 and i == ic and j == jc:
            dz[i, j] = pulse[i, j]
        
        ez[i, j] = gaz[i, j] * dz[i, j]

    cuda.syncthreads()

    if 0 < j < je - 1 and i < ie - 1:
        hx[i, j] = hx[i, j] + 0.5 * (ez[i, j] - ez[i, j + 1])

    if 0 < i < ie - 1 and j < je - 1:
        hy[i, j] = hy[i, j] + 0.5 * (ez[i + 1, j] - ez[i, j])

# Animation setup
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(range(je), range(ie))

def animate(frame):
    fdtd_cuda[blockspergrid, threadsperblock](dz_d, ez_d, hx_d, hy_d, gaz_d, ic, jc, t0, spread, frame, pulse_d)
    ez_d.copy_to_host(ez)
    
    ax.clear()
    plot_e_field(ax, ez, frame + 1)
    
    # Save the figure as a PNG image
    fig.savefig(f'frame_{frame:03d}.png')

def plot_e_field(ax, data, timestep):
    ax.set_zlim(0, 1)
    ax.view_init(elev=35., azim=135.)  # Top corner view
    ax.plot_surface(X, Y, data[:, :], cmap='jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel(r' $E_{Z}$', rotation=90, labelpad=10, fontsize=14)
    ax.set_zticks([0, 0.5, 1])
    ax.set_xlabel('cm')
    ax.set_ylabel('cm')
    ax.set_xticks(np.arange(0, 61, step=20))
    ax.set_yticks(np.arange(0, 61, step=20))
    ax.text2D(0.6, 0.7, "T = {}".format(timestep), transform=ax.transAxes)
    ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
    plt.gca().patch.set_facecolor('white')

# Perform the animation
for frame in tqdm(range(nsteps)):
    for i in range(frame/dt):
        animate(i)

# Close the figure to prevent any display
plt.close(fig)

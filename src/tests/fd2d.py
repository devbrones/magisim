import numpy as np
from math import exp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import cuda

# Parameters
ie = 60
je = 60
ic = int(ie / 2)
jc = int(je / 2)
nsteps = 60
t0 = 20
spread = 6

# CUDA setup
threadsperblock = (16, 16)
blockspergrid_x = (ie + threadsperblock[0] - 1) // threadsperblock[0]
blockspergrid_y = (je + threadsperblock[1] - 1) // threadsperblock[1]
blockspergrid = (blockspergrid_x, blockspergrid_y)

# Initialize arrays
ez = np.zeros((ie, je))
dz = np.zeros((ie, je))
hx = np.zeros((ie, je))
hy = np.zeros((ie, je))
gaz = np.ones((ie, je))
pulse = np.zeros((ie, je))
pulse[ic, jc] = 1

# CUDA functions
@cuda.jit
def fdtd_cuda(dz, ez, hx, hy, gaz, ic, jc, t0, spread, time_step, pulse):
    i, j = cuda.grid(2)

    if 0 < i < ie - 1 and 0 < j < je - 1:
        dz[i, j] = dz[i, j] + 0.5 * (hy[i, j] - hy[i - 1, j] - hx[i, j] + hx[i, j - 1])
        
        if time_step == 1 and i == ic and j == jc:  # Generate the pulse only in the first time step
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
    fdtd_cuda[blockspergrid, threadsperblock](dz, ez, hx, hy, gaz, ic, jc, t0, spread, frame, pulse)
    ax.clear()
    plot_e_field(ax, ez, frame + 1)

def plot_e_field(ax, data, timestep):
    ax.set_zlim(0, 1)
    ax.view_init(elev=20., azim=45)
    cax = ax.plot_surface(X, Y, data[:, :], cmap='jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    fig.colorbar(cax, ax=ax, pad=0.1)
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
    ax.dist = 11

ani = FuncAnimation(fig, animate, frames=nsteps, interval=200)

# Start the animation
plt.show()

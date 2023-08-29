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
nsteps = 50
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
        dz[i, j] += 0.5 * (hy[i, j] - hy[i - 1, j] - hx[i, j] + hx[i, j - 1])

        if i == ic and j == jc:
            dz[i, j] = pulse[i, j]

        ez[i, j] = gaz[i, j] * dz[i, j]

        hx[i, j] += 0.5 * (ez[i, j] - ez[i, j + 1])
        hy[i, j] += 0.5 * (ez[i + 1, j] - ez[i, j])

# Animation setup
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')

def animate(frame):
    fdtd_cuda[blockspergrid, threadsperblock](dz, ez, hx, hy, gaz, ic, jc, t0, spread, frame, pulse)
    ax.clear()
    plot_e_field(ax, ez, frame + 1, plotting_points[frame]['label'])

ani = FuncAnimation(fig, animate, frames=nsteps, interval=200)

# Function for plotting
def plot_e_field(ax, data, timestep, label):
    ax.set_zlim(0, 1)
    ax.view_init(elev=20., azim=45)
    ax.plot_surface(X, Y, data[:, :], rstride=1, cstride=1, color='white', edgecolor='black', linewidth=.25)
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
    ax.text2D(-0.2, 0.8, "({})".format(label), transform=ax.transAxes)
    ax.dist = 11

# Definition of plotting points
plotting_points = [
    {'label': 'a', 'num_steps': 20, 'data_to_plot': None},
    {'label': 'b', 'num_steps': 30, 'data_to_plot': None},
    {'label': 'c', 'num_steps': 40, 'data_to_plot': None},
    {'label': 'd', 'num_steps': 50, 'data_to_plot': None},
]

X, Y = np.meshgrid(range(je), range(ie))

# Start the animation
plt.show()

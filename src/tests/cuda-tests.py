import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numba import cuda, jit
from matplotlib.widgets import RectangleSelector

# Define the size of the image and other parameters
width, height = 800, 800
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5
max_iter = 1000
cmap = plt.cm.viridis

# Define a Numba JIT-compiled function to calculate the Mandelbrot set
@cuda.jit
def mandelbrot_set_gpu(image, width, height, x_min, x_max, y_min, y_max, max_iter):
    i, j = cuda.grid(2)
    if i < width and j < height:
        x = x_min + (x_max - x_min) * i / width
        y = y_min + (y_max - y_min) * j / height
        c = complex(x, y)
        z = complex(0.0, 0.0)
        for iter in range(max_iter):
            z = z * z + c
            if abs(z) > 2.0:
                break
        image[j, i] = iter

# Create a figure with an initial plot of the Mandelbrot set
fig, ax = plt.subplots()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_title("Mandelbrot Set")

# Allocate GPU memory for the image
image_gpu = cuda.device_array((height, width), dtype=np.uint32)

# Calculate the Mandelbrot set on the GPU
threads_per_block = (16, 16)
blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
mandelbrot_set_gpu[blocks_per_grid, threads_per_block](image_gpu, width, height, x_min, x_max, y_min, y_max, max_iter)

# Transfer the image data back to the CPU
image_cpu = image_gpu.copy_to_host()
img = ax.imshow(image_cpu, extent=(x_min, x_max, y_min, y_max), cmap=cmap, interpolation='bilinear')

# Define a callback function for rectangle selection
def on_select(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    ax.set_xlim(min(x1, x2), max(x1, x2))
    ax.set_ylim(min(y1, y2), max(y1, y2))
    mandelbrot_set_gpu[blocks_per_grid, threads_per_block](image_gpu, width, height, ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1], max_iter)
    image_cpu = image_gpu.copy_to_host()
    img.set_data(image_cpu)
    fig.canvas.draw()

# Add the rectangle selector to the plot
rect_selector = RectangleSelector(ax, on_select, drawtype='box', rectprops=dict(edgecolor='red', facecolor='none'))

plt.show()

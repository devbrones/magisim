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

# Define an event handler for zooming
def on_click(event):
    if event.button == 1:  # Left mouse button
        x_range = ax.get_xlim()
        y_range = ax.get_ylim()
        x_center = (x_range[0] + x_range[1]) / 2
        y_center = (y_range[0] + y_range[1]) / 2
        x_width = (x_range[1] - x_range[0]) / 4
        y_width = (y_range[1] - y_range[0]) / 4
        ax.set_xlim(x_center - x_width, x_center + x_width)
        ax.set_ylim(y_center - y_width, y_center + y_width)
        mandelbrot_set_gpu[blocks_per_grid, threads_per_block](
            image_gpu,
            width,
            height,
            ax.get_xlim()[0],
            ax.get_xlim()[1],
            ax.get_ylim()[0],
            ax.get_ylim()[1],
            max_iter,
        )
        image_cpu = image_gpu.copy_to_host()
        img.set_data(image_cpu)
        fig.canvas.draw()

# Connect the event handler
fig.canvas.mpl_connect("button_press_event", on_click)

plt.show()

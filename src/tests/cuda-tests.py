import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numba import cuda, jit
from matplotlib.widgets import RectangleSelector
import time

# Define the size of the image and other parameters
width, height = 800, 800
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5
max_iter = 1000
cmap = plt.cm.viridis

# Define a Numba JIT-compiled function to calculate the Mandelbrot set on CPU
@jit
def mandelbrot_set_cpu(image, width, height, x_min, x_max, y_min, y_max, max_iter):
    for i in range(width):
        for j in range(height):
            x = x_min + (x_max - x_min) * i / width
            y = y_min + (y_max - y_min) * j / height
            c = complex(x, y)
            z = complex(0.0, 0.0)
            for iter in range(max_iter):
                z = z * z + c
                if abs(z) > 2.0:
                    break
            image[j, i] = iter

# Define a Numba JIT-compiled function to calculate the Mandelbrot set on GPU
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

# Calculate the Mandelbrot set on the CPU
start_time_cpu = time.time()
image_cpu = np.empty((height, width), dtype=np.uint32)
mandelbrot_set_cpu(image_cpu, width, height, x_min, x_max, y_min, y_max, max_iter)
cpu_execution_time = time.time() - start_time_cpu

# Calculate the Mandelbrot set on the GPU
threads_per_block = (16, 16)
blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
start_time_gpu = time.time()
mandelbrot_set_gpu[blocks_per_grid, threads_per_block](
    image_gpu, width, height, x_min, x_max, y_min, y_max, max_iter
)
cuda.synchronize()
gpu_execution_time = time.time() - start_time_gpu

# Print execution times
print(f"CPU Execution Time: {cpu_execution_time:.4f} seconds")
print(f"GPU Execution Time: {gpu_execution_time:.4f} seconds")

# Transfer the image data back to the CPU
image_cpu = image_gpu.copy_to_host()
img = ax.imshow(
    image_cpu, extent=(x_min, x_max, y_min, y_max), cmap=cmap, interpolation="bilinear"
)

# Define an event handler for zooming
def on_scroll(event):
    if event.button == "up":
        factor = 0.9
    elif event.button == "down":
        factor = 1.1
    else:
        return

    x_range = ax.get_xlim()
    y_range = ax.get_ylim()
    x_center = (x_range[0] + x_range[1]) / 2
    y_center = (y_range[0] + y_range[1]) / 2
    x_width = (x_range[1] - x_range[0]) / 2
    y_width = (y_range[1] - y_range[0]) / 2
    new_x_width = x_width * factor
    new_y_width = y_width * factor

    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    new_x_min = x - (x - x_range[0]) * (new_x_width / x_width)
    new_x_max = x + (x_range[1] - x) * (new_x_width / x_width)
    new_y_min = y - (y - y_range[0]) * (new_y_width / y_width)
    new_y_max = y + (y_range[1] - y) * (new_y_width / y_width)

    ax.set_xlim(new_x_min, new_x_max)
    ax.set_ylim(new_y_min, new_y_max)

    mandelbrot_set_gpu[blocks_per_grid, threads_per_block](
        image_gpu, width, height, new_x_min, new_x_max, new_y_min, new_y_max, max_iter
    )
    image_cpu = image_gpu.copy_to_host()
    img.set_data(image_cpu)
    fig.canvas.draw()

# Connect the event handler
fig.canvas.mpl_connect("scroll_event", on_scroll)

plt.show()

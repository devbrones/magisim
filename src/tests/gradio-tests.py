import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numba import cuda, jit
import time
import gradio as gr
from PIL import Image
import io


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
def mandelbrot_visualize(cpu, gpu, width, height, x_min, x_max, y_min, y_max, max_iter):
    plt.interactive(True)  # Enable interactive mode for matplotlib
    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title("Mandelbrot Set")

    # Allocate GPU memory for the image
    image_gpu = cuda.device_array((height, width), dtype=np.uint32)

    # Calculate the Mandelbrot set on the CPU and GPU
    if cpu:
        start_time_cpu = time.time()
        image_cpu = np.empty((height, width), dtype=np.uint32)
        mandelbrot_set_cpu(image_cpu, width, height, x_min, x_max, y_min, y_max, max_iter)
        cpu_execution_time = time.time() - start_time_cpu
        print(f"CPU Execution Time: {cpu_execution_time:.4f} seconds")

    if gpu:
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
        print(f"GPU Execution Time: {gpu_execution_time:.4f} seconds")

        # Transfer the image data back to the CPU
        image_cpu = image_gpu.copy_to_host()

    ax.imshow(
        image_cpu,
        extent=(x_min, x_max, y_min, y_max),
        cmap="viridis",
        interpolation="bilinear",
    )

    # Convert the matplotlib plot to a PIL image
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    pil_img = Image.open(buf)

    # Convert the PIL image to a numpy array
    np_img = np.array(pil_img)

    plt.close()
    return np_img

iface = gr.Interface(
    fn=mandelbrot_visualize,
    inputs=[
        gr.inputs.Checkbox(default=False, label="Calculate CPU"),
        gr.inputs.Checkbox(default=True, label="Calculate GPU"),
        gr.inputs.Number(default=800, label="Width"),
        gr.inputs.Number(default=800, label="Height"),
        gr.inputs.Number(default=-2.0, label="X Min"),
        gr.inputs.Number(default=1.0, label="X Max"),
        gr.inputs.Number(default=-1.5, label="Y Min"),
        gr.inputs.Number(default=1.5, label="Y Max"),
        gr.inputs.Number(default=1000, label="Max Iter"),
    ],
    outputs=gr.outputs.Image(type="numpy"),
)

iface.launch()
import numpy as np
from numba import cuda, jit
import time
import gradio as gr

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
def measure_execution_time(cpu, gpu, width, height, x_min, x_max, y_min, y_max, max_iter):
    num_iterations = 10  # Number of iterations for averaging

    total_cpu_time = 0
    total_gpu_time = 0
    width = int(width)
    height = int(height)
    max_iter = int(max_iter)


    for _ in range(num_iterations):
        if cpu:
            image_cpu = np.empty((height, width), dtype=np.uint32)
            start_time_cpu = time.time()
            mandelbrot_set_cpu(image_cpu, width, height, x_min, x_max, y_min, y_max, max_iter)
            cpu_execution_time = time.time() - start_time_cpu
            total_cpu_time += cpu_execution_time

        if gpu:
            threads_per_block = (16, 16)
            blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
            blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
            blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
            start_time_gpu = time.time()
            image_gpu = cuda.device_array((height, width), dtype=np.uint32)
            mandelbrot_set_gpu[blocks_per_grid, threads_per_block](
                image_gpu, width, height, x_min, x_max, y_min, y_max, max_iter
            )
            cuda.synchronize()
            gpu_execution_time = time.time() - start_time_gpu
            total_gpu_time += gpu_execution_time

    average_cpu_time = total_cpu_time / num_iterations if cpu else 0
    average_gpu_time = total_gpu_time / num_iterations if gpu else 0

    return f"Average CPU Execution Time: {average_cpu_time:.4f} seconds", f"Average GPU Execution Time: {average_gpu_time:.4f} seconds"

## gradio initialization

theme = gr.themes.Base(
    primary_hue="sky",
)

iface = gr.Interface(
    fn=measure_execution_time,
    inputs=[
        gr.inputs.Checkbox(default=True, label="Calculate CPU"),
        gr.inputs.Checkbox(default=True, label="Calculate GPU"),
        gr.inputs.Number(default=800, label="Width"),
        gr.inputs.Number(default=800, label="Height"),
        gr.inputs.Number(default=-2.0, label="X Min"),
        gr.inputs.Number(default=1.0, label="X Max"),
        gr.inputs.Number(default=-1.5, label="Y Min"),
        gr.inputs.Number(default=1.5, label="Y Max"),
        gr.inputs.Number(default=1000, label="Max Iter"),
    ],
    outputs=[
        gr.outputs.Textbox(label="CPU Time"),
        gr.outputs.Textbox(label="GPU Time"),
    ],
)

with gr.Blocks() as iface:
    with gr.Row():
        cp_time = gr.outputs.Textbox(label="CPU Time")
        gp_time = gr.outputs.Textbox(label="GPU Time")
    
    with gr.Column():
        gr.Label("CPU", gradio_style=theme)
        
        gr.Label("GPU", gradio_style=theme)
    
    with gr.Column():    
        gr.Label("Width", gradio_style=theme)
        gr.Label("Height", gradio_style=theme)
        gr.Label("X Min", gradio_style=theme)
        gr.Label("X Max", gradio_style=theme)
        gr.Label("Y Min", gradio_style=theme)
        gr.Label("Y Max", gradio_style=theme)
        gr.Label("Max Iter", gradio_style=theme)
    
    



iface.launch(share=True)
import gradio as gr
import numpy as np

class grid:
    width: int
    height: int
    depth: int
    grid: np.ndarray
    
class object:
    position: tuple
    model: gr.Model3D
    output: gr.Model3D
    
def load_model(mesh_filename: str):
    return mesh_filename


with gr.Blocks() as gui:
    with gr.Tab("Welcome"):
        #
        
        gr.Markdown("# Magisim\ -\ Electromagnetic\ Simulation\ Software")
        
    with gr.Tab("Workspace"):
        # Workspace
        with gr.Column():
            object.model = gr.Model3D()
            object.output = gr.Model3D(clear_color=[0.0, 0.0, 0.0, 0.0],  label="3D Model")
        with gr.Column():
            grid.height = gr.Slider(minimum=1, maximum=100, step=1, default=10, label="Height")
            grid.width = gr.Slider(minimum=1, maximum=100, step=1, default=10, label="Width")
            grid.depth = gr.Slider(minimum=1, maximum=100, step=1, default=10, label="Depth")
            grid.grid = np.zeros((grid.height, grid.width, grid.depth))
            
            
        
        
    with gr.Tab("Settings"):
        # Settings
        with gr.Column():
            gr.Label("Settings")

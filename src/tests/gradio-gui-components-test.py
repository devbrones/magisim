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
        with gr.Row():
            object.model = gr.Model3D()
            with gr.Box():
                grid.height = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Height")
                grid.width = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Width")
                grid.depth = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Depth")
                #grid.grid = np.zeros((int(grid.height), int(grid.width), int(grid.depth)))
    with gr.Tab("Settings"):
        # Settings
        with gr.Column():
            gr.Label("Settings")
gui.launch(share=True)
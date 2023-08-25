import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

class grid:
    width: int
    height: int
    depth: int
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
    
class object:
    position: tuple
    model: gr.Model3D
    output: gr.Model3D
    

def display_plot(h,w,d):
    # make sure plot is empty
    plt.clf()
    # create grid
    grid.width = w
    grid.height = h
    grid.depth = d
    grid.x,grid.y = np.meshgrid(np.linspace(-w/2,w/2,d),np.linspace(-h/2,h/2,d))
    grid.u = grid.x/np.sqrt(grid.x**2 + grid.y**2)
    grid.v = grid.y/np.sqrt(grid.x**2 + grid.y**2)
    # return matplotlib plot
    plt.quiver(grid.x,grid.y,grid.u,grid.v)
    return plt
    
    
def load_model(mesh_filename: str):
    return mesh_filename


with gr.Blocks() as gui:
    gr.Markdown("""
                <img src="/file=magisim_logo256.png" alt="Description" width="5%">
                
                <h1>Magisim</h1>""")
    with gr.Tab("Welcome"):
        #
        
        gr.Markdown("# Magisim\nElectromagnetic Simulation Software")
        
    with gr.Tab("Workspace"):
        # Workspace
        with gr.Row():
            with gr.Column():
                object.model = gr.Model3D()
                with gr.Box():
                    h = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Height")
                    w = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Width")
                    d = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Depth")
                    #grid.grid = np.zeros((int(grid.height), int(grid.width), int(grid.depth)))
            with gr.Column():
                plot = gr.Plot(label="Field")
                update_btn = gr.Button(label="Update")
            
    update_btn.click(display_plot,[h,w,d], plot)
                
                
                
    with gr.Tab("Settings"):
        # Settings
        with gr.Column():
            gr.Label("Settings")
gui.launch(share=True)
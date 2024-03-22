# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
import shapeloader.shapeloader as ShapeLoader
# no imports #


class ExtensionMeta:
	name: str = "ShapeLoader"
	uuid: str = "0604d7bc-323a-4af4-8408-946f643b9bcb"
	authors: list = ["devbrones"]
	version: str = "1.0.3"
	license: str = "LGPL3"
	description: str = """ Load 3D models as numpy arrays """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Editor] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
		hasSettings: bool = False # can be set to be checked by a function later if needed
  
def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		with gr.Column():
			with gr.Row():
				#shape = gr.Model3D()
				upload = gr.File(label="Upload shape",type="file",description="Upload a 2D model in .dxf format", file_types=[".dxf"])
				shape = gr.Image()
				with gr.Box():
					modeselector = gr.Dropdown(["1D (single cut)", "2D (multi cut)", "3D (not supported)"],label="Dimension",info="Change the cut dimension (if nD<3) or full cut (3D)")
					res = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Resolution")
					cutpoint = gr.Slider(minimum=-50, maximum=50, value=0, label="Cut point (relative to center of model) [%]")
					xpos = gr.Number(label="X position, relative to source [m]")
					ypos = gr.Number(label="Y position, relative to source [m]")

		with gr.Column():
			with gr.Row():
				plot = gr.Plot(label="Space")
				load_btn = gr.Button(label="Load", variant="primary")
				update_btn = gr.Button(label="Update", variant="secondary")	
					
	load_btn.click(ShapeLoader.ShapeLoader.load_input,[upload, modeselector , res, cutpoint, xpos, ypos], shape, scroll_to_output=True, show_progress='full')
	update_btn.click(ShapeLoader.ShapeLoader.create_result,[upload, modeselector , res, cutpoint, xpos, ypos], plot, scroll_to_output=True, show_progress='full')

            
# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
import extensions.extension_880843c55c42.epsilon as epsilon 
# no imports #


class ExtensionMeta:
	name: str = "Epsilon0"
	uuid: str = "d8b29835-ad56-4d0c-90b6-880843c55c42"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.0"
	license: str = "LGPL3"
	description: str = """ FDTD simulator """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Simulator] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
		hasSettings: bool = True # can be set to be checked by a function later if needed
  
def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		with gr.Column():
			with gr.Row():
				sim = gr.Plot(label="Simulation")
				with gr.Box():
					amp = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Amplitude")
					freq = gr.Slider(minimum=0, maximum=500, value=30, label="Frequency")
					xpos = gr.Number(label="X position of source [m]")
					ypos = gr.Number(label="Y position of source [m]")

		with gr.Column():
			with gr.Row():
				space = gr.Plot(label="Space")
				update_btn = gr.Button(label="Update", variant="primary")		
	update_btn.click(epsilon.Simulator.run,[sim, amp , freq, space, xpos, ypos], sim, scroll_to_output=True, show_progress='full')

        


            
# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
import extensions.extension_caed19de0a8b.openmsems as ems 

# no imports #


class ExtensionMeta:
	name: str = "MSEMS"
	uuid: str = "20e4e311-43e1-4c3f-af70-caed19de0a8b"
	authors: list = ["devbrones"]
	version: str = "0.0.0"
	license: str = "LGPL3"
	description: str = """ OpenEMS integration for Magisim """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Simulator, Extension.Workspace] # list of classes
		layoutCompat: bool = False
		# externalNodes: str = "nodes.js" ## TODO: implement this later so developers can define their own nodes in js!
		hasNodes: [(Extension,(list,list))] = [(Extension.Simulator, ([("Source Position X","number"),
																       ("Source Position Y","number"), 
																	   ("Wavelength","number"),
																	   ("Frequency","number"),
																	   ("Phase","number"),
																	   ("Amplitude (dB)","number"),
																	   ("Domain","np2d"),
																	   ("Object","np2d"),
																	   ("Simple Object","np2d"),
                                                                       ("PML","np2d")],
																	  [("Frequency Domain","np2d"),
					                                                   ("Time Domain","np2d"),
																	   ("E","np2d"),
																	   ("H","np2d")])),
																	   (Extension.Editor, ([("Sim Space","np2d")],[("Domain","np2d"), ("Object","np2d"), ("PML","np2d")]))]
		hasSettings: bool = True # can be set to be checked by a function later if needed

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		with gr.Column():
			with gr.Row():
				sim = gr.Plot(label="Simulation")
				with gr.Row():
					simpleObjectMu = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Simple Object Mu")
					simpleObjectEpsilon = gr.Slider(minimum=0, maximum=500, value=30, label="Simple Object Epsilon")
					options = gr.CheckboxGroup(["Simple Object"], label="Object")
		with gr.Column():
			with gr.Row():
				space = gr.Plot(label="Space")
				update_btn = gr.Button(value="Update", variant="primary")
		
		update_btn.click(ems.sendtest)
        


            
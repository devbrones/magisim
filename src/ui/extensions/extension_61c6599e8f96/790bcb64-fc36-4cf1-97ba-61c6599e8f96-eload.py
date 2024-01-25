# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
import extensions.extension_61c6599e8f96.visualizer as vis

# no imports #


class ExtensionMeta:
	name: str = "Visualizer"
	uuid: str = "790bcb64-fc36-4cf1-97ba-61c6599e8f96"
	authors: list = ["devbrones"]
	version: str = "0.0.1"
	license: str = "LGPL3"
	description: str = """ Simple Matplot Visualizer """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Renderer] # list of classes
		layoutCompat: bool = False
		# externalNodes: str = "nodes.js" ## TODO: implement this later so developers can define their own nodes in js!
		hasNodes: [(Extension,(list,list))] = [(Extension.Renderer, ([("Plot","matplot")],[]))]
		hasSettings: bool = True # can be set to be checked by a function later if needed

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		vis.get_visualizer(app)
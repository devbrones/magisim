# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
import extensions.extension_caed19de0a8b.openmsems as ems 

# no imports #


class ExtensionMeta:
	name: str = "MSEMS"
	uuid: str = "20e4e311-43e1-4c3f-af70-caed19de0a8b"
	authors: list = ["devbrones"]
	version: str = "1.1"
	license: str = "LGPL3"
	description: str = """ FDTD Simulator for Magisim """

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		with gr.Group():
			with gr.Row():
				slid = gr.Slider(minimum=0, maximum=100, step=1, label="Slid")
				butt = gr.Button(text="Butt")
				


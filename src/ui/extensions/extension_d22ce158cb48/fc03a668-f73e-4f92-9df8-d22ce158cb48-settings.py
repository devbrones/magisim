# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
import extensions.extension_d22ce158cb48.analyzer as anal # ;) 

# no imports #


class ExtensionMeta:
	name: str = "Analyzer"
	uuid: str = "fc03a668-f73e-4f92-9df8-d22ce158cb48"
	authors: list = ["devbrones"]
	version: str = "0.0.0"
	license: str = "LGPL3"
	description: str = """ Analyze numpy arrays """

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)


# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
from greeter.greeter import Greeter
import greeter.external.docs as docs
import greeter.hub.hub as hub

class ExtensionMeta:
	name: str = "Magisim"
	uuid: str = "24645031-d7fd-4bf8-bdb4-472b0d26b3a9"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.1-devel"
	license: str = "LGPL3"
	description: str = """ Welcome to Magisim """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Builtin] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
            
def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name, id="greetertab"):
		with gr.Tab("Projects"):
			#Greeter.load_workspace(app)
			gr.Markdown("Welcome to Magisim")
			gr.Markdown("# Open Project")
			gr.FileExplorer("Open Project", "file", "open_project")
			gr.Markdown("## Create New Project by making changes and saving them")

		with gr.Tab("Hub"):
			hub.load_workspace(app)
		with gr.Tab("Documentation"):
			docs.load_workspace(app)

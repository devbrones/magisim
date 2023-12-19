# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
import greeter.greeter as greeter
import greeter.external.docs as docs

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
	with gr.TabItem(ExtensionMeta.name):
		with gr.TabItem("Projects", id="builtin_greetertab"):
			greeter.load_workspace(app)
		with gr.TabItem("Documentation", id="builtin_doctab"):
			docs.load_workspace(app)

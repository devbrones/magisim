# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
from nodemgr.nodemgr import NodeManager

class ExtensionMeta:
	name: str = "Nodes"
	uuid: str = "f53f499f-1ec9-41be-9edc-050d81f4313b"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.1-devel"
	license: str = "LGPL3"
	description: str = """ Nodes """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Builtin] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
            
def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name,elem_id="nmgrtab"):
		gr.Markdown(ExtensionMeta.description)
		#load the node manager
		with gr.Column():
			NodeManager.fetch_node_save_button() # this is the greatest achievement so far in this project.
			nmgr: gr.HTML = NodeManager.fetch_node_editor()
			with gr.Column():
				interface_nmgr_reload = gr.Button(Config.Icon.refresh_symbol+"Reload Nodes", interactive=False)				
				gr.Checkbox(label=str(Config.Icon.warning_symbol+"Advanced Mode"))
				gr.CheckboxGroup(["Debug Mode","Use Math Nodes","Show Builtin Nodes","Show Node UUIDs"], label="Advanced Properties", interactive=False)
				
		#with gr.Column(scale=0.5):
			

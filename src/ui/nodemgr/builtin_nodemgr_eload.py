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
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		#load the node manager
		with gr.Row(min_height=600):
			NodeManager.fetch_node_editor()
			with gr.Column(min_width=200):
				interface_nmgr_save = gr.Button(Config.Icon.save_style_symbol+"Save Nodes", interactive=True, variant="primary")
				interface_nmgr_reload = gr.Button(Config.Icon.refresh_symbol+"Reload Nodes", interactive=False)				
				gr.Checkbox(label=str(Config.Icon.warning_symbol+"Advanced Mode"), inline=True)
				gr.CheckboxGroup(["Debug Mode","Use Math Nodes","Show Builtin Nodes","Show Node UUIDs","Custom API"], label="Advanced Properties", inline=True, interactive=False)


				with gr.Accordion(label="Custom API", open=False, elem_id="interface_nmgr_advanced_property_custom_api_accordion"):
					interface_nmgr_advanced_property_custom_api_url = gr.Textbox(label="URL")
					interface_nmgr_advanced_property_custom_api_key = gr.Textbox(label="Key")

		#with gr.Column(scale=0.5):
			

# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
from settingsmgr.settingsmgr import SettingsManager

class ExtensionMeta:
	name: str = "Settings Manager"
	uuid: str = "b6619c08-d0fe-41a6-83b7-89483f8ffd9c"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.1-devel"
	license: str = "LGPL3"
	description: str = """ Settings Manager """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Builtin] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
            
def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name, id="settingsmgrtab"):
		gr.Markdown(ExtensionMeta.description)
		with gr.Accordion("NodeManager"):
			gr.Markdown("# NodeManager specific settings")
			do_autoload = gr.Checkbox("Autoload NodeManager", value=True)
			show_advanced_settings = gr.Checkbox("Show advanced settings", value=False)
		
		with gr.Accordion("ExtensionManager"):
			gr.Markdown("# ExtensionManager specific settings")
			do_refresh_on_reload = gr.Checkbox("Auto Refresh ExtensionManager on reload", value=False)
			show_advanced_settings = gr.Checkbox("Show advanced settings", value=False)

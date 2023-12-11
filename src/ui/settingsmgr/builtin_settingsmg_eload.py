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
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		SettingsManager.get_settings_menu(app)

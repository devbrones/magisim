# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config
class ExtensionMeta:
	name: str = "Magisim Documentation"
	uuid: str = "24645031-d7fd-4bf8-bdb4-472b0d26b3a9"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.1-devel"
	license: str = "LGPL3"
	description: str = """ Read our documentation """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Builtin] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
		
class Hub:
	def get_hub():
		iframe = f"""
         <iframe src="https://magisim.mintlify.app" title="Magisim Docs"></iframe> 
"""
		return gr.HTML(iframe)

            
def load_workspace(app: gr.Blocks):
	gr.Markdown(ExtensionMeta.description)
	Hub.get_hub()
    
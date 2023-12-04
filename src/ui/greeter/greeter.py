# TODO: https://www.gradio.app/docs/fileexplorer for project explorer
# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config
class ExtensionMeta:
	name: str = "Magisim"
	uuid: str = "24645031-d7fd-4bf8-bdb4-472b0d26b3a9"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.9.2"
	license: str = "LGPL3"
	description: str = """Magisim (MAGisim-Is-a-SIMulator)"""
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Builtin] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
		
class Greeter:
#	def greeter():
#        gr.Markdown("Welcome to Magisim")

    def get_project_folder():
        return Config.project_folder

            
def load_workspace(app: gr.Blocks):
	gr.Markdown(ExtensionMeta.description)
	#projects = gr.FileExplorer(file_count="single", root=Greeter.get_project_folder(), glob="*.mse", label="Open Project")
	file = gr.FileExplorer()
    
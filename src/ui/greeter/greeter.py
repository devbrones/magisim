# TODO: https://www.gradio.app/docs/fileexplorer for project explorer
# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config
from shared.projectmanager import projectmanager
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
	landimg = gr.Image("shared/banner1.png",
                      label=None, show_label=False, elem_id="banner",
                      show_download_button=False, container=False)
	projects = gr.FileExplorer(file_count="single", root=Greeter.get_project_folder(), glob="*.mse", label="Local Projects")
	#file = gr.FileExplorer()
	# load project button
	with gr.Row():
		lpbutton = gr.Button(f"{Config.Icon.open_file_symbol} Load Project", variant="primary")
		npbutton = gr.Button(f"{Config.Icon.new_file_symbol}New Project", variant="secondary")
	with gr.Row():
		rpbutton = gr.Button("Download Remote Project", variant="secondary", icon="shared/github.png", interactive=False)
		dpbutton = gr.Button(f"{Config.Icon.bin_symbol} Delete Project", variant="stop")
    
	# button functions

	# load project
	lpbutton.click(projectmanager.load_project(projects))
	# new project
	npbutton.click(projectmanager.new_project())
	# delete project
	dpbutton.click(projectmanager.delete_project(projects))
	# download project
	#rpbutton.click(projectmanager.download_project())

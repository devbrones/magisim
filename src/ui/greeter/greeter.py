# TODO: https://www.gradio.app/docs/fileexplorer for project explorer
# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config
from shared.projectmanager import projectmanager 
import extensionmgr.extensionmgr as emgr

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
	landimg = gr.Image("shared/banner1-short.png",
                      label=None, show_label=False, elem_id="banner",
                      show_download_button=False, container=False)
	# if no extensions are installed, show the install extensions modal
	if len(emgr.get_extensions()) == 0:
		# show the install extensions modal
		with gr.Group():
			gr.HTML("<h2 style='text-align: center; !important'>You don't have any extensions installed, visit the extension marketplace or install an extension using the extension manager</h2>", )
			gr.Button("Extension Marketplace", variant="secondary", link="https://magisim.com")

	projects = gr.FileExplorer(file_count="single", root_dir=Greeter.get_project_folder(), glob="*.mse", label="Local Projects")
	#file = gr.FileExplorer()
	# load project button
	with gr.Row():
		with gr.Row():
			lpbutton = gr.Button(f"{Config.Icon.open_file_symbol} Load Project", variant="primary")
			projname = gr.Textbox(show_label=False, placeholder="Project Name", visible=False, container=False, interactive=True)
		with gr.Row():
			npbutton = gr.Button(f"{Config.Icon.new_file_symbol}New Project", variant="secondary")
			cfbutton = gr.Button(f"{Config.Icon.new_file_symbol}New Project", variant="primary", visible=False)
			# when the user clicks the new project button, hide the new project button and show the confirm button, hide the load project button and show the project name textbox
			npbutton.click(lambda :[gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)], None, [npbutton, cfbutton])
			npbutton.click(lambda :[gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)], None, [lpbutton, projname])
			# when the user clicks the confirm button, execute the new project function and hide the confirm button and project name textbox, show the load project button
			cfbutton.click(lambda :[gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)], None, [npbutton, cfbutton])
			cfbutton.click(lambda :[gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)], None, [lpbutton, projname])
			cfbutton.click(projectmanager.new_project, inputs=[projname])


	with gr.Row():
		with gr.Row():
			rpbutton = gr.Button("Download Remote Project", variant="secondary", icon="shared/github.png", interactive=False)
		with gr.Row():
			dpbutton = gr.Button(f"{Config.Icon.bin_symbol} Delete Project", variant="stop")
			confirm_btn = gr.Button("Confirm delete", variant="stop", visible=False)
			cancel_btn = gr.Button("Cancel", visible=False)
			dpbutton.click(lambda :[gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)], None, [dpbutton, confirm_btn, cancel_btn])
			cancel_btn.click(lambda :[gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)], None, [dpbutton, confirm_btn, cancel_btn])
    

	# button functions

	# load project
	lpbutton.click(projectmanager.load_project, inputs=[projects])
	# new project
	#npbutton.click(projectmanager.new_project)
	# delete project
	dpbutton.click(projectmanager.delete_project, inputs=[projects])
	# download project
	#rpbutton.click(projectmanager.download_project())

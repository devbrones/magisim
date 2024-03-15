# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
import extensions.extension_caed19de0a8b.openmsems as ems 
from extensions.extension_caed19de0a8b.settings import Settings
# no imports #


class ExtensionMeta:
	name: str = "MSEMS"
	uuid: str = "20e4e311-43e1-4c3f-af70-caed19de0a8b"
	authors: list = ["devbrones"]
	version: str = "1.1"
	license: str = "LGPL3"
	description: str = """ FDTD Simulator for Magisim """

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		# some settings that we can change in the settingsmanager
		# i.e. the max number of iterations, the grid max size, etc.
		# we will change the settings file for this extension

		# settings
		with gr.Group():
			Settings.max_iterations = gr.Number(1000, label="Max Iterations", maximum=100000, step=1, interactive=True)
			Settings.grid_max_size_x = gr.Number(1000, label="Grid Max Size X", maximum=100000, step=1, interactive=True)
			Settings.grid_max_size_y = gr.Number(1000, label="Grid Max Size Y", maximum=100000, step=1, interactive=True)
			Settings.grid_max_size_z = gr.Number(1000, label="Grid Max Size Z", maximum=100000, step=1, interactive=True)

				


# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
from extensionmgr.extensionmgr import extract_and_run

class ExtensionMeta:
	name: str = "Extension Manager"
	uuid: str = "7b7584a4-86ea-4076-9da4-1c3813605059"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.1-devel"
	license: str = "LGPL3"
	description: str = """ Magisim's built in extension manager lets you install and manage extensions for Magisim. """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Builtin] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
  
def load_workspace():
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        zip_file = gr.File(label="Upload a ZIP file")
        run_button = gr.Button("Install")
        output_text = gr.Textbox()
        run_button.click(extract_and_run, inputs=[zip_file], outputs=[output_text])
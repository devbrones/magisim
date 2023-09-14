# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
# no imports #


class ExtensionMeta:
	name: str = "ExtensionMagic"
	uuid: str = "0a119a6d-7f36-4c6c-929b-50812d1e265b"
	authors: list = ["devbrones","thegregster1111"]
	version: str = "0.0.69"
	license: str = "LGPL3"
	description: str = """ IM GOIGN INSANE """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Editor] # list of classes
		layoutCompat: bool = False
		hasNodes: list = []
  
def load_workspace():
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        with gr.Row():
            zip_file = gr.File(label="Upload a ZIP file") 
        with gr.Row():
            run_button = gr.Button("Install")
            output_text = gr.Textbox()
            
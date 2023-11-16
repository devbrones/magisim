# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
from extensionmgr.extensionmgr import extract_and_run, get_extensions
import os
import threading
import sys
import subprocess

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


def load_workspace(app: gr.Blocks):
    with gr.Tab(ExtensionMeta.name, id="extensionmgrtab"):
        gr.Markdown(ExtensionMeta.description)
        zip_file = gr.File(label="Upload a ZIP file")
        run_button = gr.Button("Install")
       	#reload_button = gr.Button(Config.Icon.refresh_symbol + " Reload", interactive=False)
        output_text = gr.Textbox()
        run_button.click(extract_and_run, inputs=[zip_file], outputs=[output_text])
		# list of installed extensions
        installed_extensions_df = gr.Dataframe(headers=["Name", "Version", "Author", "Description", "Active"], interactive=False, value=get_extensions())

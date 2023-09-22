# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
from extensionmgr.extensionmgr import extract_and_run
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

# Shared variable to signal a UI reload
reload_requested = False
reload_lock = threading.Lock()

## Function to restart the UI
#def restart_ui():
#    # Start a new UI process with stdin, stdout, and stderr connected to the current process
#    subprocess.Popen([sys.executable, "ui.py"], stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)

def load_workspace(app: gr.Blocks):
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        zip_file = gr.File(label="Upload a ZIP file")
        run_button = gr.Button("Install")
#        reload_button = gr.Button(Config.Icon.refresh_symbol + " Reload", interactive=False)
        output_text = gr.Textbox()
        run_button.click(extract_and_run, inputs=[zip_file], outputs=[output_text])
        
        # Add a click handler for the Reload button
#        reload_button.click(trigger_reload)

## Function to set the reload_requested flag
#def trigger_reload():
#    global reload_requested
#    with reload_lock:
#        reload_requested = True
#        restart_ui()  # Restart the UI process without using signals
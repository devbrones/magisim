# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
#import extensions.extension_7716380cda41.harmony as harmony

# no imports #


class ExtensionMeta:
    name: str = "Harmony"
    uuid: str = "88ad74c6-39e1-491b-818c-7716380cda41"
    authors: list = ["devbrones"]
    version: str = "0.0.0-dt1"
    license: str = "LGPL3"
    description: str = """ We are all waves! """
	# nhr meta
    class ExtensionType:
        types: list = [Extension.Editor] # list of classes
        layoutCompat: bool = False
        hasNodes: [(Extension,(list,list))] = [ (Extension.Transform, ( [ ("Raw Data (WAV)","file"), ("EDF (1ch)","file") ],[ ("A","np1d"), ("B","np1d"), ("C","np1d"), ("D","np1d"), ("E","np1d"), ("F","np1d")] ) ) ]

def load_workspace(app: gr.Blocks):
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        with gr.Row():
            
        
            
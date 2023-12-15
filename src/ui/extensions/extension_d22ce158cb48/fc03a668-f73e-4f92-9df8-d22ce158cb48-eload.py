# shared extension imports
import gradio as gr
from shared.builtin import Extension
import extensionmgr.extensionmgr as emgr
from shared.config import Config


# extension specific imports
import extensions.extension_d22ce158cb48.analyzer as anal # ;)

# no imports #


class ExtensionMeta:
    name: str = "Analyzer"
    uuid: str = "fc03a668-f73e-4f92-9df8-d22ce158cb48"
    authors: list = ["devbrones"]
    version: str = "0.0.0"
    license: str = "LGPL3"
    description: str = """ Analyze numpy arrays """
	# nhr meta
    class ExtensionType:
        types: list = [Extension.Editor] # list of classes
        layoutCompat: bool = False
        hasNodes: [(Extension,(list,list))] = [(Extension.Simulator,([("Numpy Object", "np")],[("Result","matplot")]))]


def load_workspace(app: gr.Blocks):
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        with gr.Row():
            with gr.Column():
                with gr.Accordion(label="Raw Data"):
                    rdata = gr.Code()
                with gr.Accordion(label="Plotted Data"):
                    pdata = gr.Plot()
            with gr.Column():
                gr.Markdown("Data Properties")
                # checkboxes and dropdowns where the user can select what type the data is of. this will be handled later
                # by the shared.datatype module. Each extension will have a python file containing a description of its
                # associated data types. this will be used to determine what type of data the user is working with.
                
                ex_selector = gr.Dropdown(label="Extension", choices=emgr.get_extensions())


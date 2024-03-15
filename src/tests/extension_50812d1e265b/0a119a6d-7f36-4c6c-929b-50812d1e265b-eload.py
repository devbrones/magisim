# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
import extensions.extension_50812d1e265b.extensionmagic as extensionmagic
from extensions.extension_50812d1e265b.extensionmagic_node import ExtensionNode

# no imports #


class ExtensionMeta:
    name: str = "ExtensionMagic"
    uuid: str = "0a119a6d-7f36-4c6c-929b-50812d1e265b"
    authors: list = ["devbrones","thegregster1111"]
    version: str = "0.0.69"
    license: str = "LGPL3"
    description: str = """ IM GOIGN INSANE """
    ExNode: ExtensionNode = ExtensionNode(uuid, name, "simulator/ExtensionMagic")
	# nhr meta
    class ExtensionType:
        types: list = [Extension.Editor] # list of classes
        layoutCompat: bool = False
        hasNodes: [(Extension,(list,list))] = [(Extension.Simulator,([("Space", "number"),
                                                                      ("Sensitivity","number"),
                                                                      ("Frequency","number"),
                                                                      ("ypos","number"),
                                                                      ("xpos","number"),
                                                                      ("amplitude","number")],
                                                                      [("graph","number"),
                                                                       ("video","number"),
                                                                       ("fft","number")
                                                                       ])), (Extension.Editor,([("xpos","number"),
                                                                                                ("ypos","number")],
                                                                                                [("Space","number")]))]


def load_workspace(app: gr.Blocks):
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        with gr.Row():
            gr.Markdown("Hello from ExtensionMagic!")
            extension_name = gr.Textbox()
        run_extension_fn = gr.Button("get message")
        run_extension_fn.click(extensionmagic.run_extension, outputs=[extension_name])


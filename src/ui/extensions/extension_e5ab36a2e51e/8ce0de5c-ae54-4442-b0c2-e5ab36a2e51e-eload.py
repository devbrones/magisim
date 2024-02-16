# shared extension imports
import gradio as gr
from shared.builtin import Extension

# extension specific imports
import extensions.extension_e5ab36a2e51e.stlloader as stlloader
# no imports #


class ExtensionMeta:
    name: str = "STLLoader"
    uuid: str = "8ce0de5c-ae54-4442-b0c2-e5ab36a2e51e"
    authors: list = ["devbrones"]
    version: str = "0.1"
    license: str = "LGPL3"
    description: str = """ Load a STL file into 3D space or a 2D slice """
	# nhr meta
    class ExtensionType:
        types: list = [Extension.Editor] # list of classes
        layoutCompat: bool = False
        hasNodes: [(Extension,(list,list))] = [(Extension.Output,([], # no inputs (be slice later)
                                                                      [("2D","array2d"),
                                                                       ("3D","array3d")]))]
def load_workspace(app: gr.Blocks):
    with gr.Tab(ExtensionMeta.name):
        gr.Markdown(ExtensionMeta.description)
        with gr.Row():
            with gr.Column():
                stlfile = gr.Model3D()
                slicder = gr.Slider(minimum=0, maximum=300, step=1, label="Slice Position")
                max_size = gr.Number(label="Max Size")
                with gr.Group():
                    gr.Label("Rotation in Degrees")
                    xro = gr.Number(label="X")
                    yro = gr.Number(label="Y")
                    zro = gr.Number(label="Z")
            with gr.Column():
                res = gr.Plot()
        startbtn = gr.Button("Start")
        savebtn = gr.Button("Save as MSO")
        output_file = gr.File(label="Output File")
        startbtn.click(stlloader.convert2d, inputs=[stlfile, slicder, max_size, xro, yro, zro], outputs=res)
        savebtn.click(stlloader.save, inputs=[stlfile, slicder, max_size, xro, yro, zro], outputs=output_file)


import gradio as gr
import magisim_config
def read(x):
    with open(x.name) as fo:
        return fo.read()

magisim_main_application = gr.Blocks(**magisim_config.BaseConfig.uiArgs())

with magisim_main_application: ## main interface - gradio blocks
    file = gr.File()
    upload = gr.Button('Upload')
    data = gr.Textbox(label='Data')
    upload.click(read, inputs=[file], outputs=[data])

magisim_main_application.launch()
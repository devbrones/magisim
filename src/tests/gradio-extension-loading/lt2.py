import gradio as gr



def test(zip_file):
    return f"Hello, {zip_file.name}!"

def loadElements():
    argarr: list = []
    zf = gr.File(label="Upload a ZIP file")
    rb = gr.Button("Run")
    ot = gr.Textbox()
    rbc = rb.click(test, inputs=[zf], outputs=[ot])
    argarr.append(zf)
    argarr.append(rb)
    argarr.append(ot)
    argarr.append(rbc)
    
    
    return argarr


# Define the Gradio interface
with gr.Blocks() as app:
    loadElements()

# Launch the Gradio application
app.launch()
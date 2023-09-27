# my_module.py
import gradio as gr

# Define a function for the Gradio interface
def greet(name):
    return f"Hello, {name}!"

# Create a Gradio interface with the function
iface = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(),
    outputs=gr.Textbox(),
    live=True,
    title="Greeting POOP",
    description="Enter your name to get a POOP!",
)

# Launch the Gradio interface
iface.launch()

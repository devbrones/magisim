import gradio as gr

class info:
    name: str = "Text Size Extension"
    type: str = "visualizer"
    author: str = "Gradio"
    requirements: str = "None"
    
    

class TextSizeExtension:
    def __init__(self):
        self.text_size = 20  # Default text size
        self.tab = gr.Tab(
            "Text Size Extension",
            gr.Input("user_input", type="text"),
            gr.Slider("text_size_slider", min=10, max=50, step=1, default=self.text_size, label="Text Size"),
            gr.Output("output_text", type="text", label="Output"),
            fn=self.extension_function,
        )

    def extension_function(self, user_input, text_size_slider):
        # Update the text size based on the slider value
        self.text_size = text_size_slider

        # Apply the updated text size to the displayed text
        result = f"<span style='font-size: {self.text_size}px'>{user_input}</span>"

        return result

# If this module is run directly, it acts as a standalone Gradio interface for testing the extension.
if __name__ == "__main__":
    extension = TextSizeExtension()
    interface = gr.Interface(extension.tab)
    interface.launch()

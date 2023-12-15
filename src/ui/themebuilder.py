import gradio as gr


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Tab():
                gr.Markdown("Welcome to the NHR IDE!")
                gr.Markdown("This is a work in progress, so expect bugs.")
                gr.Markdown("If you find any, please report them on the GitHub page.")
            with gr.Tab():
                gr.Markdown("This is the second tab.")
                gr.Markdown("It's empty right now.")
                gr.Markdown("We'll add more content later.")
    
        with gr.Column(scale=0):
            gr.Markdown("This is a column with a scale of 0.")

demo.launch()
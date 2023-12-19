import plotly.express as px
import gradio as gr
import numpy as np
import time

"""
This is a test to see if I can get a plotly graph to update live in a gradio interface. and also make sure it keeps its zoom level and stuff.
 - I need to note that the plot will be an image, so I need to make sure that the image is updated and not the plot itself.
"""
def update_plot():
    # while loop that yields a new plotly figure every second
    # cretae a figure (heatmap)
    # lets make a simple heatmap
    # edit: holy fuck it works!
    while True:
        fig = px.imshow(np.random.rand(10, 10))
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig['layout']['uirevision'] = 'some-constant'
        time.sleep(1)
        yield fig



def load_ui(app: gr.Blocks):

    # lets make a gradio interface
    gr.Markdown("Plotly live update test")
    plot = gr.Plot(label="Plot")
    startbtn = gr.Button("Start")
    startbtn.click(update_plot, None, plot)





with gr.Blocks() as app:
    load_ui(app)


app.launch()
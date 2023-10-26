import gradio as gr
from shared.config import Config
import json

litegraph_css = ""
with open("nodemgr/static/css/litegraph.css", "r") as f:
    litegraph_css = f.read()


class NodeManager:

    def fetch_node_editor():
        nmgr_html = f"""
        <html>
            <head>    
                <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
                <style>
                    { litegraph_css }
                </style>
            </head>
            <body>
                <div style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; background-color: red;" id='nodeGraphContainer'>
                    <canvas id='nodecanvas' width='100px' height='100px'></canvas>
                    <img src onerror='startNodeGraph()'>
                </div>
            </body>
        </html>
        """

        
        gr.HTML(nmgr_html)


    def fetch_node_save_button():
        nbtn_html = f"""
        <html>
            <head>    
                <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
            </head>
            <body>
                <button style="width: 100%;" class="lg primary svelte-1ipelgc" onclick="graph.pushgraph()">{ Config.Icon.save_style_symbol }Save Nodes</button>
            </body>
        </html>
        """
        gr.HTML(nbtn_html)

    def update_local_node_cache(input: str):
        # convert the input json to a dict
        nodes = json.loads(input)
        # process the data
        
        


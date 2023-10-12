import gradio as gr

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

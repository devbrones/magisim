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
                <div min-height='600px'>
                    <canvas id='nodecanvas' width='100%' height='100%'></canvas>
                    
                    <img src onerror='startNodeGraph()'>
                </div>
            </body>
        </html>
        """

        
        gr.HTML(nmgr_html)

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
                <div>
                    <canvas id='nodecanvas' width='1024' height='720' style='border: 1px solid'></canvas>
                </div>
            </body>
        </html>
        """

        
        gr.HTML(nmgr_html)

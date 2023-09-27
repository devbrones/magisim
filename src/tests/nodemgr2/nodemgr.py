import gradio as gr

litegraph_js = ""
with open("nodemgr/static/js/litegraph.js", "r") as f:
    litegraph_js = f.read()

litegraph_css = ""
with open("nodemgr/static/css/litegraph.css", "r") as f:
    litegraph_css = f.read()


class NodeManager:
    def fetch_node_script():
        return f"""
        <script>
            { litegraph_js }
        </script>
        <script>
                console.log("litegraph is loading")
                var graph = new LGraph();

                var canvas = new LGraphCanvas("#nodecanvas", graph);

                var node_const = LiteGraph.createNode("basic/const");
                node_const.pos = [200, 200];
                graph.add(node_const);
                node_const.setValue(4.5);

                var node_watch = LiteGraph.createNode("basic/watch");
                node_watch.pos = [700, 200];
                graph.add(node_watch);

                node_const.connect(0, node_watch, 0);

                graph.start()
            </script>
            """
    
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
                    <p>Node Editor</p>
                    <canvas id='nodecanvas' width='1024' height='720' style='border: 1px solid'></canvas>
                </div>
            </body>
        </html>
        """

        
        gr.HTML(nmgr_html)

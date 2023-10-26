import gradio as gr
from shared.config import Config
import extensionmgr.extensionmgr as emgr
from shared.builtin import Extension
from shared.logger import Logger
import json


litegraph_css = ""
with open("nodemgr/static/css/litegraph.css", "r") as f:
    litegraph_css = f.read()

nmgrlog = Logger("NodeManager")

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

    def generate_node_db():
        nodedb: str = ""
        # get the list of loaded extensions
        loaded_extensions = emgr.get_loaded_extensions()
        # iterate through the extensions and get the list of nodes
        for ext in loaded_extensions:
            if ext.ExtensionMeta.ExtensionType.hasNodes == []:
                nmgrlog.logger.info(f"Skipping node generation for extension {ext.ExtensionMeta.name} because it has no nodes")
                continue
            nodes: [(Extension,(list,list))] = ext.ExtensionMeta.ExtensionType.hasNodes # [(Extension.Simulator,([<INPUTS>(name,type)],[<OUTPUTS>(name,type)])), (Extension.Editor([inputs],[outputs]))]
            # generate a node for each node in the extension
            for node in nodes:
                nodeindex = nodes.index(node)
                nodeuuid = "node_" + str(nodeindex) + "_" + ext.ExtensionMeta.uuid.split("-")[-1]
                if Config.debug:
                    nmgrlog.logger.debug(f"Generating node for {node[0]}")
                # generate a node based on class and respective inputs and outputs
                # generate the node class
                ipts: str = ""
                for ipt in node[1][0]: 
                    ipts += f"this.addInput('{ipt[0]}','{ipt[1]}');"
                #if Config.debug:
                #    nmgrlog.logger.debug(f"ipts: {ipts}")

                opts: str = ""
                for opt in node[1][1]: 
                    opts += f"this.addOutput('{opt[0]}','{opt[1]}');"
                #if Config.debug:
                #    nmgrlog.logger.debug(f"opts: {opts}")

                node_class = f"""
                //node constructor class
                function {nodeuuid}()
                {{
                    {ipts}
                    {opts}
                  this.properties = {{ precision: {str(Config.Compute.presicion)} }};
                }}
                
                //name to show
                {nodeuuid}.title = "{ext.ExtensionMeta.name}";
                
                //function to call when the node is executed
                {nodeuuid}.prototype.onExecute = function()
                {{
                  
                }}
                
                //register in the system
                LiteGraph.registerNodeType("basic/{str(node[0]).split(".")[-1][:-3]}", {nodeuuid} );
                """
                #if Config.debug:
                #    nmgrlog.logger.debug(f"node_class: {node_class}")

                nodedb += node_class
        return nodedb
    
    def update_local_node_cache(input: str):
        # convert the input json to a dict
        nodes = json.loads(input)
        # process the data
        
        


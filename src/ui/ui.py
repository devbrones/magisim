import gradio as gr
from shared.config import Config
from fastapi import FastAPI, Request
from starlette.responses import Response


# builtin extension imports
import extensionmgr.builtin_extensionmgr_eload as builtin_extensionmgr_eload 
import extensionmgr.extensionmgr as emgr
import settingsmgr.builtin_settingsmg_eload as builtin_settingsmgr_eload
import settingsmgr.settingsmgr as smgr
import nodemgr.builtin_nodemgr_eload as builtin_nodemgr_eload
import nodemgr.nodemgr as nmgr


fapp = FastAPI()
litegraph_js = ""
with open("nodemgr/static/js/litegraph.js", "r") as f:
    litegraph_js = f.read()

@fapp.middleware("http")
async def some_fastapi_middleware(request: Request, call_next):
    ## Middleware to inject litegraph.js into the index.html because gradio does not support custom js lol
    # god bless the original author of this code, i cannot remember who it was but i love you
    response = await call_next(request)
    path = request.scope["path"]
    if path == "/":
        response_body = ""
        async for chunk in response.body_iterator:
            response_body += chunk.decode()

        some_javascript = f"""
        <script type="text/javascript" id="lgscr">
        { litegraph_js }
        </script>
        """

        some2_javascript = f"""
        <script>
            var graph;
            var canvas;
            function startNodeGraph() {{
                var div = document.getElementById('nodeGraphContainer');
                var canvas = document.getElementById('nodecanvas');
                var divWidth = div.offsetWidth;
                var divHeight = div.offsetHeight;
                canvas.width = divWidth;
                canvas.height = divHeight;
                
                /*canvas.addEventListener('resize', () => {{
                    canvas.width = document.getElementById('nodeGraphContainer').offsetWidth;
                    canvas.height = document.getElementById('nodeGraphContainer').offsetHeight;
                }});*/
                
                graph = new LGraph();

                canvas = new LGraphCanvas("#nodecanvas", graph);

                graph.start()
            }}
        </script>
        """ # this will literally never load in properly lol 
            # 230927 EDIT: it does now, but does not scale properly
            


        response_body = response_body.replace("</head>", some_javascript + some2_javascript + "</head>")

        del response.headers["content-length"]

        return Response(
            content=response_body,
            status_code=response.status_code, 
            headers=dict(response.headers),
            media_type=response.media_type
        )

    return response

def load_ui(app: gr.Blocks):
    # load the builtin node manager
    builtin_nodemgr_eload.load_workspace(app) # load the node manager
    ## iterate through all extensions and load their UIs through their eload modules
    # get a list of all installed extensions and their paths
    extensions = emgr.get_installed_extensions()
    # iterate through all extensions and load their UIs through their eload modules
    for extension in extensions:
        loaded_extension = emgr.get_extension_eload(extension)
        if loaded_extension is not None or str:
            try:
                loaded_extension.load_workspace()
            except Exception as e:
                print(e)
                return None
        else:
            print("Error: Failed to load extension: " + extension)
            return None
    # load the builtin extension manager
    builtin_extensionmgr_eload.load_workspace(app) # load the extension manager
    # load the builtin settings manager
    builtin_settingsmgr_eload.load_workspace(app) # load the settings manager

# Define the Gradio interface
with gr.Blocks(theme=Config.UI.theme) as app:
    ## they did not say i could do this - but i did it anyway!
    load_ui(app)

# Launch the Gradio application
#app.launch(server_port=Config.UI.port)
gr.mount_gradio_app(fapp, app, path="/")

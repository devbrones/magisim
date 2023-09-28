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
    """
    The function `some_fastapi_middleware` is a FastAPI middleware that injects litegraph.js into the
    index.html response to enable custom JavaScript functionality.
    
    :param request: The `request` parameter is an instance of the `Request` class from the `fastapi`
    module. It represents the incoming HTTP request that is being processed by the middleware
    :type request: Request
    :param call_next: `call_next` is a callable that represents the next middleware or the endpoint
    handler. It is responsible for processing the request and generating a response. In the context of
    FastAPI middleware, `call_next` is typically an asynchronous function that takes a `Request` object
    as input and returns a `Response
    :return: The middleware function returns a modified response object. If the path is "/", the
    function injects litegraph.js and some additional JavaScript code into the HTML response body. It
    then returns a new Response object with the modified response body, status code, headers, and media
    type. If the path is not "/", the function simply returns the original response object.
    """
    ## Middleware to inject litegraph.js into the index.html because gradio does not support custom js lol
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
            function startNodeGraph() {{
                var graph = new LGraph();

                var canvas = new LGraphCanvas("#nodecanvas", graph);

                var node_const = LiteGraph.createNode("basic/const");
                node_const.pos = [200,200];
                graph.add(node_const);
                node_const.setValue(4.5);

                var node_watch = LiteGraph.createNode("basic/watch");
                node_watch.pos = [700,200];
                graph.add(node_watch);

                node_const.connect(0, node_watch, 0 );

                graph.start()
            }}
        </script>
        """ # this will literally never load in properly


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
    """
    The function `load_ui` loads the user interface for a given application, including the builtin node
    manager, extensions, extension manager, and settings manager.
    
    :param app: The "app" parameter is an instance of the gr.Blocks class. It represents the application
    or workspace where the UIs will be loaded
    :type app: gr.Blocks
    :return: The function does not return anything.
    """
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

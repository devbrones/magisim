import gradio as gr
from shared.config import Config
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import Response
import torch
from shared.router import Router
import os
from shared.logger import Logger
from shared.item import Item
from shared.projectmanager import projectmanager


# builtin extension imports
import extensionmgr.builtin_extensionmgr_eload as builtin_extensionmgr_eload 
import extensionmgr.extensionmgr as emgr
import settingsmgr.builtin_settingsmg_eload as builtin_settingsmgr_eload
import settingsmgr.settingsmgr as smgr
import nodemgr.builtin_nodemgr_eload as builtin_nodemgr_eload
import nodemgr.nodemgr as nmgr
import greeter.builtin_greeter_eload as builtin_greeter_eload
import greeter.greeter as greeter


#import shapeloader.builtin_shapeloader_eload as builtin_shapeloader_eload
#import shapeloader.shapeloader as sloadr

# Pre-Startup checks

# Check if a CUDA compatible GPU is available
# If not, print a warning and continue but set config flag to False

Config.Compute.CUDA.isAvailable = torch.cuda.is_available()
if Config.Compute.CUDA.isAvailable:
    Config.Compute.CUDA.device = torch.cuda.current_device()
    Config.Compute.CUDA.name = torch.cuda.get_device_name(Config.Compute.CUDA.device)
    Config.Compute.CUDA.memory = torch.cuda.get_device_properties(0).total_memory
else:
    Config.Compute.CPU.cores = os.cpu_count()
    Config.Compute.CPU.memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # mem in kb



fapp = FastAPI()

# set up the custom endpoints for nodegraph as well as shape loading

apilog = Logger("FastAPI")
nodelog = Logger("NodeManager-Preload")

@fapp.post("/api/nodeg-update")
async def nodeg_post(item: Item):
    # Print the contents of the request to the command line
    apilog.logger.info("Received nodegraph update")
    uuid_1 = "caed19de0a8b"
    uuid_2 = "50812d1e265b"
    Router.establish_tunnel(uuid_1, uuid_2)
    status = Router.update_nodes(item)
    return status[0][0]

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

        nodes: str = nmgr.NodeManager.generate_node_db() ## outputs a string that contains all the node definitions


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
                }});*/ // replace with a resize viewport event listener, canvas should be fullpage
                
                graph = new LGraph();

                canvas = new LGraphCanvas("#nodecanvas", graph);

                graph.start()
                LiteGraph.clearRegisteredTypes() // remove default graph types
                // register extension graph nodes
                
                { nodes }

            }}

        /**
     *
     * Wait for an HTML element to be loaded like `div`, `span`, `img`, etc.
     * ex: `onElementLoaded("div.some_class").then(()=>{{}}).catch(()=>{{}})`
     * @param {{*}} elementToObserve wait for this element to load
     * @param {{*}} parentStaticElement (optional) if parent element is not passed then `document` is used
     * @return {{*}} Promise - return promise when `elementToObserve` is loaded
     */
    function onElementLoaded(elementToObserve, parentStaticElement) {{
      const promise = new Promise((resolve, reject) => {{
        try {{
          if (document.querySelector(elementToObserve)) {{
            console.log(`element already present: ${{elementToObserve}}`);
            resolve(true);
            return;
          }}
          const parentElement = parentStaticElement
            ? document.querySelector(parentStaticElement)
            : document;

          const observer = new MutationObserver((mutationList, obsrvr) => {{
            const divToCheck = document.querySelector(elementToObserve);

            if (divToCheck) {{
              console.log(`element loaded: ${{elementToObserve}}`);
              obsrvr.disconnect(); // stop observing
              resolve(true);
            }}
          }});

          // start observing for dynamic div
          observer.observe(parentElement, {{
            childList: true,
            subtree: true,
          }});
        }} catch (e) {{
          console.log(e);
          reject(Error("some issue... promise rejected"));
        }}
      }});
      return promise;
    }}


            
        </script>
        """ # this will literally never load in properly lol 
            # 230927 EDIT: it does now, but does not scale properly

        some3_javascript = """
        var has_loaded = false;
        
        // this will run last
        
        // change display: none to display: block of div id nmgrtab after 100ms
        setTimeout(() => {
            console.log("Loading node manager...")
            document.getElementById("nmgrtab").style.display = "block";
            startNodeGraph();
        }, 3500);
        // change it back after 100ms
        setTimeout(() => {
            console.log("Finished loading node manager...")
            document.getElementById("nmgrtab").style.display = "none";
        }, 3800);


        """

        reps = """
			const ce = document.getElementsByTagName("gradio-app");
			if (ce[0]) {
				ce[0].addEventListener("domchange", () => {
					document.body.style.padding = "0";
				});
				document.body.style.padding = "0";
			}
		"""

        response_body = response_body.replace('<script>window.gradio_config', some_javascript + some2_javascript + '<script>window.gradio_config')
        response_body = response_body.replace(reps, reps + some3_javascript)

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
    
    with gr.Row():
        # sidebar menu
        #
        with gr.Column(scale=0):    
            with gr.Accordion(label="File", open=False):
                with gr.Group():
                    savebutton = gr.Button(f"Save", variant="primary", size="sm", elem_classes=["sbitem"])
                    loadbutton = gr.Button(f"Load", variant="secondary", size="sm", elem_classes=["smitem"])

            with gr.Accordion(label="Edit", open=False):
                gr.Markdown("Edit")


            with gr.Accordion(label="View", open=False):
                gr.Markdown("View")

            with gr.Accordion(label="Help", open=False):
                with gr.Group():
                    helpbutton = gr.Button(f"Help", variant="secondary", size="sm", elem_classes=["smitem"])
                    docsbutton = gr.Button(f"Docs", variant="secondary", size="sm", elem_classes=["smitem"])
                    debugbutton = gr.Button(f"Debug", variant="secondary", size="sm", elem_classes=["smitem"])
                    aboutbutton = gr.Button(f"About", variant="secondary", size="sm", elem_classes=["smitem"])

            # active node view
            with gr.Group():
                gr.Markdown("Active Extensions")
                exbox = gr.Textbox(placeholder="Active Extensions", elem_classes=["exbox"], interactive=False)
                values = ""
                for extension in emgr.get_installed_extensions():
                    values += extension + "\n"  
                exbox.value = values
                    
                

            # debug command line
            with gr.Group():
                debugconsole = gr.Code(label="", show_label=False, language="python", elem_classes=["debugconsole"], lines=10, interactive=False, container=False)
                debuginput = gr.Text(placeholder="Debug Command", elem_classes=["debuginput"], interactive=True)
                debugbutton = gr.Button(f"Run", variant="secondary", size="sm", elem_classes=["debugbutton"])


        with gr.Column(scale=5):
            builtin_greeter_eload.load_workspace(app) # load the greeter
            builtin_nodemgr_eload.load_workspace(app) # load the node manager

            ## iterate through all extensions and load their UIs through their eload modules
            # get a list of all installed extensions and their paths
            extensions = emgr.get_installed_extensions()
            # iterate through all extensions and load their UIs through their eload modules
            for extension in extensions:
                loaded_extension = emgr.get_extension_eload(extension)
                if loaded_extension is not None or str:
                    try:
                        loaded_extension.load_workspace(app)
                    except Exception as e:
                        print("GOT EXCEPTION")
                        print(e)
                        continue
                else:
                    print("Error: Failed to load extension: " + extension)
                    continue

            print("Loaded all extensions")
            # load the builtin extension manager
            builtin_extensionmgr_eload.load_workspace(app) # load the extension manager
            # load the builtin settings manager
            builtin_settingsmgr_eload.load_workspace(app) # load the settings manager
            #builtin_shapeloader_eload.load_workspace(app) # load the shapeloader
        
    
    
css = ""
with open("shared/globalcss.css", "r") as cssf:
    css=cssf.read()
# Define the Gradio interface
with gr.Blocks(theme=Config.UI.theme, css=css) as app:
    ## they did not say i could do this - but i did it anyway!
    # magisim logo on the left side and title on right side using row
    gr.Image("shared/magisim_logo256.png",
                label=None, show_label=False, width=64,height=64, elem_id="logo",
                show_download_button=False, container=False)
    load_ui(app)

    # add footer using svelte footer, only with name and small logo
    
# Launch the Gradio application
#app.launch(server_port=Config.UI.port)
gr.mount_gradio_app(fapp, app, path="/")

import gradio as gr
from shared.config import Config

# builtin extension imports
import extensionmgr.builtin_extensionmgr_eload as builtin_extensionmgr_eload 
import extensionmgr.extensionmgr as emgr
import settingsmgr.builtin_settingsmg_eload as builtin_settingsmgr_eload
import settingsmgr.settingsmgr as smgr


def load_ui(app: gr.Blocks):
    ## iterate through all extensions and load their UIs through their eload modules
    # get a list of all installed extensions and their paths
    extensions = emgr.get_installed_extensions()
    # iterate through all extensions and load their UIs through their eload modules
    for extension in extensions:
        loaded_extension = emgr.get_extension_eload(extension)
        print("got loaded_extension: " + str(loaded_extension))
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
with gr.Blocks() as app:
    ## they did not say i could do this - but i did it anyway!
    load_ui(app)

# Launch the Gradio application
app.launch(server_port=Config.UI.port)

import gradio as gr
import extensionmgr.builtin_extensionmgr_eload as builtin_extensionmgr_eload 
import extensionmgr.extensionmgr as extensionmgr

def load_ui():
    ## iterate through all extensions and load their UIs through their eload modules
    # get a list of all installed extensions and their paths
    extensions = extensionmgr.get_installed_extensions()
    # iterate through all extensions and load their UIs through their eload modules
    for extension in extensions:
        loaded_extension = extensionmgr.import_extension(extension)
        if loaded_extension is not None:
            ## get the eload
            pass
            

    builtin_extensionmgr_eload.load_workspace() # load the extension manager

# Define the Gradio interface
with gr.Blocks() as app:
    ## they did not say i could do this - but i did it anyway!
    load_ui()

# Launch the Gradio application
app.launch()

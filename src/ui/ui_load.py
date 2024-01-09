import gradio as gr



# builtin extension imports
import extensionmgr.builtin_extensionmgr_eload as builtin_extensionmgr_eload 
import extensionmgr.extensionmgr as emgr
import settingsmgr.builtin_settingsmg_eload as builtin_settingsmgr_eload
import settingsmgr.settingsmgr as smgr
import nodemgr.builtin_nodemgr_eload as builtin_nodemgr_eload
import nodemgr.nodemgr as nmgr
import greeter.builtin_greeter_eload as builtin_greeter_eload
import greeter.greeter as greeter

def doctabloader():
    return gr.Tabs(selected="builtin_doctab")


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
             ## they did not say i could do this - but i did it anyway!
            # magisim logo on the left side and title on right side using row
            with gr.Row():
                gr.HTML("<img src='file/shared/magisim_logo256.png' width='32' height='32' style='margin-right: 10px; margin-left: 10px;'></img>")
                
                gr.Markdown("# magisim", label="", show_label=False) 
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
                    gr.Markdown("*this is not implemented correctly, if your screen blanks, just reload the page*")
                    docsbutton = gr.Button(f"Docs", variant="secondary", size="sm", elem_classes=["smitem"])
                    debugbutton = gr.Button(f"Debug", variant="secondary", size="sm", elem_classes=["smitem"])
                    aboutbutton = gr.Button(f"About", variant="secondary", size="sm", elem_classes=["smitem"])

            # active node view
            with gr.Group():
                aexlabel = gr.Label("Active Extensions", label="", show_label=False, container=False, visible=False)
                exbox = gr.Textbox(placeholder="Active Extensions", elem_classes=["exbox"], interactive=False, lines=len(emgr.get_installed_extensions()), visible=False)
                values = ""
                for extension in emgr.get_installed_extensions():
                    values += extension + "\n"  
                exbox.value = values
                    
            # tunnelview
            with gr.Group():
                gr.Label("TunnelView", label="", show_label=False, container=False)
                tvplot = gr.Plot(label="", show_label=False, container=False)
                tvrefr = gr.Button(f"Refresh", variant="secondary", size="sm", elem_classes=["smitem"])


            # debug command line
            with gr.Group():
                debugconsole = gr.Code(label="", show_label=False, language="python", elem_classes=["debugconsole"], lines=10, interactive=False, container=False,visible=False)
                debuginput = gr.Text(placeholder="Debug Command", elem_classes=["debuginput"], interactive=True, visible=False)
                debugbutton = gr.Button(f"Run", variant="secondary", size="sm", elem_classes=["debugbutton"], visible=False)

            


        with gr.Column(scale=5):
            with gr.Tabs() as main_tabbed_window:
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

                #docsbutton.click(js="/*open docs in new tab*/ window.open('https://magisim.mintlify.app/', '_blank') ")
                # switch to builtin_doctab when docs button is clicked
                docsbutton.click(doctabloader, None, main_tabbed_window)
    # debug actions
    # if the debug button is pressed, show the debug console and the loaded extensions
    # npbutton.click(lambda :[gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)], None, [npbutton, cfbutton])
    debugbutton.click(lambda :[gr.update(visible=True)], None, [aexlabel, exbox, debugconsole, debuginput, debugbutton])

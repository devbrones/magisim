import gradio as gr
import importlib
import os

# Define the directory where your modules are located
module_directory = "loaded-exts"

# Get a list of all Python files in the directory that end with "-module.py"
module_files = [f for f in os.listdir(module_directory) if f.endswith("-module.py")]

# Create a list to store interfaces
interfaces = []

# Import and load each module as an interface
for module_file in module_files:
    print("got module_file: " + module_file)
    module_name = module_directory + "." + module_file[:-3]  # Remove ".py" extension
    module_path = os.path.join(module_directory, module_file)
    loaded_module = importlib.import_module(module_name)
    if hasattr(loaded_module, "iface"):  # Check if the module has an interface
        interfaces.append(loaded_module.iface)  # Assuming you have an 'iface' variable in your extensions

# Create a new Gradio Interface
iface = gr.Interface(
    fn=None,  # This is just a placeholder since you're adding tabs with loaded interfaces
    title="Custom Blocks Interface",
    description="A custom interface with blocks from loaded modules",
)

# Create a new tab in the interface and add interfaces to it
tab = gr.Interface(
    fn=None,  # This is just a placeholder since you're adding blocks from the loaded modules
    title="Custom Blocks",
    description="Blocks from loaded modules",
)

for interface in interfaces:
    tab.add(interface)

# Add the tab to the main interface
iface.add(tab)

# Launch the interface
iface.launch()

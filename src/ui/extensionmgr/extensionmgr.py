import os
import importlib
import zipfile
from pathlib import Path
from shared.config import Config
import gradio as gr
# Define the extraction folder
extraction_folder = "extensions"

loaded_extensions = []


def extract_and_run(zip_file, reload_button):
    try:
        print("got extract_and_run")
        # Create the extraction folder if it doesn't exist
        try:
            Path(extraction_folder).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Failed to create extraction folder: {extraction_folder}")
        # Extract the uploaded zip file
        extracted_folder = ""
        with zipfile.ZipFile(zip_file.name, 'r') as zip_ref:
            print("extracting...")
            zip_ref.extractall(extraction_folder)
            # get the extracted folder name
            extracted_folder = zip_ref.namelist()[0]

        # Find and import the specific Python file
        for filename in os.listdir(extraction_folder + "/" + extracted_folder):
            print("got filename: " + filename)
            if filename.endswith("-eload.py"):
                print("got eload: " + filename)
                module_path = os.path.join(extraction_folder, extracted_folder, filename)
                module_name = module_path.replace("/", ".").replace(".py", "")
                print("got module_path: " + module_path)
                print("got module_name: " + module_name)
                # Import the module
                try:
                    eload_module = importlib.import_module(module_name)
                except Exception as e:
                    print(e)
                    return f"Error: Failed to import the module: {module_name}"
                # Check if the module has the 'eload' class and 'load_extension_meta' method
                if hasattr(eload_module, "eload") and hasattr(eload_module.eload, "load_extension_meta"):
                    print("got eload_module")
                    # Call the 'load_extension_meta' method
                    extension_meta = eload_module.eload.load_extension_meta()
                    return f"Extension loaded successfully. Meta: {extension_meta}"
                else:
                    return "Error: The loaded module does not have the required class or method.", gr.Button.update(reload_button, interactive=True)
        
        return "Error: No suitable Python file found in the uploaded zip."
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_extension_eload(extension_name):
    print("i gee and got extension_name: " + extension_name)
    for filename in os.listdir(extension_name.replace(".", "/")):
        print("i gee and got extension: " + filename)
        if filename.endswith("-eload.py"):
            print("i gee and got eload: " + filename)
            module_path = os.path.join(extension_name.replace(".","/"), filename)
            module_name = module_path.replace("/", ".").replace(".py", "")
            print("i gee and got module_path: " + module_path)
            print("i gee and got module_name: " + module_name)
            # Import the module
            try:
                print("i gee and got - trying to import module: " + module_name)
                eload_module = importlib.import_module(module_name)
                return eload_module
            except Exception as e:
                print("i gee and got: " + str(e))
                return f"Error: Failed to import the module: {module_name} | {str(e)}"
    
    
def get_installed_extensions() -> list:
    # get a list of all installed extensions and their paths
    extensions = []
    for extension in os.listdir(extraction_folder):
        if os.path.isdir(os.path.join(extraction_folder, extension)):
            extensions.append(os.path.join(extraction_folder, extension).replace("/", ".").replace(".py", ""))
            print("got extension: " + extensions[-1])
    print ("got extensions: " + str(extensions))
    return extensions

def get_loaded_extensions() -> list:
    return loaded_extensions

#def import_extension(extension_name):
#    try:
#        ## find the extension's eload module
#        extension_eload = get_extension_eload(extension_name)
#        print("got extension_eload: " + extension_eload)
#        # Import the module
#        
#    except Exception as e:
#        print(e)
#        return None
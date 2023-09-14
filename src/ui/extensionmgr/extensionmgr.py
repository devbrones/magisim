import os
import importlib
import zipfile
from pathlib import Path
# Define the extraction folder
extraction_folder = "extensions"

loaded_extensions = []


def extract_and_run(zip_file):
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
                print("got module_name: " + module_name)
                print("got module_path: " + module_path)
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
                    return "Error: The loaded module does not have the required class or method."
        
        return "Error: No suitable Python file found in the uploaded zip."
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_extension_eload(extension_name):
    for filename in os.listdir(extraction_folder + "/" + extension_name):
        print("got extension: " + filename)
        if filename.endswith("-eload.py"):
            print("got eload: " + filename)
            module_path = os.path.join(extraction_folder, extension_name, filename)
            module_name = module_path.replace("/", ".").replace(".py", "")
            print("got module_name: " + module_name)
            print("got module_path: " + module_path)
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
                return "Error: The loaded module does not have the required class or method."
        
        return "Error: No suitable Python file found in the uploaded zip."
    
    
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

def import_extension(extension_name):
    try:
        extension_module = importlib.import_module(extension_name)
        
        loaded_extensions.append((extension_module))
        return extension_module
    except Exception as e:
        print(e)
        return None
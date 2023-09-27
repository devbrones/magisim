import os
import importlib
import zipfile
from pathlib import Path
from shared.config import Config
from shared.logger import Logger
import gradio as gr
# Define the extraction folder
extraction_folder = "extensions"

loaded_extensions = []

# set up logger
logger = Logger("ExtensionMgr")


def extract_and_run(zip_file, reload_button):
    try:
        # Create the extraction folder if it doesn't exist
        try:
            Path(extraction_folder).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.logger.error(f"Failed to create extraction folder: {extraction_folder}")
        # Extract the uploaded zip file
        extracted_folder = ""
        with zipfile.ZipFile(zip_file.name, 'r') as zip_ref:
            zip_ref.extractall(extraction_folder)
            # get the extracted folder name
            extracted_folder = zip_ref.namelist()[0]

        # Find and import the specific Python file
        for filename in os.listdir(extraction_folder + "/" + extracted_folder):
            if filename.endswith("-eload.py"):
                module_path = os.path.join(extraction_folder, extracted_folder, filename)
                module_name = module_path.replace("/", ".").replace(".py", "")
                if Config.debug:
                    logger.logger.debug(f"Installing module: {module_name} from {module_path}")
                # Import the module
                try:
                    eload_module = importlib.import_module(module_name)
                except Exception as e:
                    logger.logger.error(f"Failed to import the module: {module_name} | {str(e)}")
                    return f"Error: Failed to import the module: {module_name}"
                if hasattr(eload_module, "ExtensionMeta"):
                    metaobj: dict = {}
                    metaobj["name"] = eload_module.ExtensionMeta.name
                    metaobj["uuid"] = eload_module.ExtensionMeta.uuid
                    metaobj["authors"] = eload_module.ExtensionMeta.authors
                    metaobj["version"] = eload_module.ExtensionMeta.version
                    metaobj["license"] = eload_module.ExtensionMeta.license
                    metaobj["description"] = eload_module.ExtensionMeta.description
                    metaobj["extension_type"] = eload_module.ExtensionMeta.ExtensionType.types
                    return metaobj
                else:
                    logger.logger.info(f"The module: {module_name} does not contain any metadata, it will load and work as expected, but wont display any information.")
                    return f"Info: The module: {module_name} does not contain any metadata, it will load and work as expected, but wont display any information."
        
        return "Error: No suitable Python file found in the uploaded zip."
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_extension_eload(extension_name):
    for filename in os.listdir(extension_name.replace(".", "/")):
        if filename.endswith("-eload.py"):
            module_path = os.path.join(extension_name.replace(".","/"), filename)
            module_name = module_path.replace("/", ".").replace(".py", "")
            if Config.debug:
                logger.logger.debug(f"Importing module: {module_name} from {module_path}")
            # Import the module
            try:
                eload_module = importlib.import_module(module_name)
                return eload_module
            except Exception as e:
                logger.logger.error(f"Failed to import the module: {module_name} | {str(e)}")
                return f"Error: Failed to import the module: {module_name} | {str(e)}"
    
    
def get_installed_extensions() -> list:
    # get a list of all installed extensions and their paths
    extensions = []
    for extension in os.listdir(extraction_folder):
        if os.path.isdir(os.path.join(extraction_folder, extension)):
            extensions.append(os.path.join(extraction_folder, extension).replace("/", ".").replace(".py", ""))
            if Config.debug:
                logger.logger.debug(f"Found extension: {extensions[-1]}")
    return extensions

def get_loaded_extensions() -> list:
    return loaded_extensions

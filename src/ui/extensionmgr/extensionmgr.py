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


def extract_and_run(zip_file):
    """
    The function `extract_and_run` extracts an extension zip file, finds its associated eload file, imports
    the module, and returns metadata about the module if it exists.
    
    :param zip_file: The `zip_file` parameter is the tempfile object of the uploaded zip file.
    :return: The function `extract_and_run` returns different values based on certain conditions. If the function fails to extract the zip file, it returns `Error: Failed to extract the zip file.`. If the function fails to find a suitable Python file, it returns `Error: No suitable Python file found in the uploaded zip.`. If the function fails to import the module, it returns `Error: Failed to import the module: {module_name} | {str(e)}`. If the function fails to find any metadata, it returns `Info: The module: {module_name} does not contain any metadata, it will load and work as expected, but wont display any information.`. If the function succeeds, it returns a dictionary containing the metadata of the module.
    """
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
    """
    The function `get_extension_eload` imports a module with a specific naming convention and returns
    the imported module.
    
    :param extension_name: The `extension_name` parameter is a string that represents the name of the
    extension. It should be in the format of a Python module name.
    :return: The function `get_extension_eload` returns the imported module `eload_module` if it is
    successfully imported. If there is an error during the import process, it returns an error message
    string indicating the failure to import the module.
    """
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
    """
    The function `get_installed_extensions` returns a list of all installed extensions.
    :return: The function `get_installed_extensions` returns a list of installed extensions.
    """
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

def get_extensions() -> list:
    pass

def load_extension_node(extension_name):
    exts = get_loaded_extensions()
    if extension_name in exts:
        try:
            eload_module = get_extension_eload(extension_name)
            if hasattr(eload_module, "get_node"):
                node_contents = eload_module.get_node()
                if Config.debug:
                    logger.logger.info(f"Loaded extension node: {extension_name}")
            else:
                logger.logger.info(f"Skipping extension node-loading for: {extension_name} | No nodes")
                return None
            return node_contents
        except Exception as e:
            logger.logger.error(f"Failed to load extension node: {extension_name} | {str(e)}")
    else:
        logger.logger.error(f"Failed to load extension node: {extension_name} | Extension not loaded")
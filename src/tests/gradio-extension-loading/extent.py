import gradio as gr
import os
import zipfile
import importlib
from pathlib import Path

# Define the extraction folder
extraction_folder = "extensions"

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

def load_ui():
    with gr.Tab("Upload Extension"):
        gr.Markdown("Upload a ZIP file containing your extension.")
        zip_file = gr.File(label="Upload a ZIP file")
        run_button = gr.Button("Run")
        output_text = gr.Textbox()
        run_button.click(extract_and_run, inputs=[zip_file], outputs=[output_text])

    
    
    
    


# Define the Gradio interface
with gr.Blocks() as app:
    load_ui()

# Launch the Gradio application
app.launch()

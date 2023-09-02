import gradio as gr
import importlib
import os
import tempfile
import uuid

# Folder where extension files are stored
extensions_folder = "extensions"

def load_extension(file):
    print("got file:" + file[0].name)
    try:
        with open(file[0].name, "r") as f:
            # print contents
            print(f.read())
    except Exception as e:
        print(e)
    """       
    try:
        # Generate a unique filename using UUID
        file_name = f"{str(uuid.uuid4())}.py"
        file_path = os.path.join(extensions_folder, file_name)

        # Write the uploaded content to the file
        with open(file_path, "wb") as f:
            print(file)
            # f.write(file.read())

        # Extract the module name without the file extension
        module_name = os.path.splitext(file_name)[0]

        # Import the module dynamically using importlib
        extension_module = importlib.import_module(module_name)

        # Check if the extension class exists in the module
        if hasattr(extension_module, module_name):
            extension_instance = getattr(extension_module, module_name)()

            # Extract information from the "info" class
            info = {
                "Name": extension_instance.name,
                "Type": extension_instance.type,
                "Author": extension_instance.author,
                "Requirements": extension_instance.requirements
            }

            return extension_instance, info
        else:
            return None, None

    except Exception as e:
        print(file)
        print(f"Failed to load extension: {file.filename}")
        return None, None
        """

# Main application
with gr.Blocks() as main_app:
    gr.Markdown("Extension Upload and Load Example")

    # File Upload Tab
    with gr.Tab("Upload Extension"):
        upload_button = gr.UploadButton("Click to Upload an Extension", file_count="multiple", file_types=[".py"])
        upload_button.upload(load_extension, upload_button)

    # Information Tab
    with gr.Tab("Extension Information"):
        info_text = gr.Textbox("Extension Information", placeholder="Information will appear here")

# Launch the main Gradio Blocks application
if __name__ == "__main__":
    main_app.launch()

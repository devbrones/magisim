import gradio as gr
from shared.config import Config
from nodemgr.nodemgr import NodeManager
from shared.router import Router

class projectmanager:
    def load_project(project_path: str):
        print(f"""got project to load: {project_path}""")

    def new_project(project_name: str):
        file_name = ""
        if project_name is None or project_name == "":
            return
        if project_name[-4:] == ".mse":
            file_name = project_name
        else:
            file_name = f"""{project_name}.mse"""

        # create project file
        


    def delete_project(project_path: str):
        pass

    def save_project():
        print("save project")
        pass



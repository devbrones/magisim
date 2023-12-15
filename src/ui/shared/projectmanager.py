import gradio as gr
from shared.config import Config
from nodemgr.nodemgr import NodeManager
from shared.router import Router

class projectmanager:
    def load_project(project_path: str):
        print(f"""got project to load: {project_path}""")

    def new_project(project_name: str):
        if project_name is None or project_name == "":
            print(f"""Got nothing, skipping""")
            return
        print(f"""got project to create: {project_name}""")
        if project_name[-4:] == ".mse":
            print(f"""with extension""")
        else:
            print(f"""without extension""")

    def delete_project(project_path: str):
        pass

    def save_project():
        print("save project")
        pass



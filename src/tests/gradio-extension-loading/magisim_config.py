import gradio as gr

class BaseConfig:
    theme: gr.themes.ThemeClass = gr.themes.Glass()
    title: str = "Magisim Development Interface"
    def __init__(self):
        pass
    def uiArgs(self):
        return {
            "theme": self.theme,
            "title": self.title,
        }
    
    
    

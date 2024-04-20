import gradio as gr
class Config:
    debug: bool = True
    
    class Icon:
        refresh_symbol = '\U0001f504'  # 🔄
        save_style_symbol = '\U0001f4be'  # 💾
        apply_style_symbol = '\U0001f4cb'  # 📋
        bin_symbol = '\U0001f5d1\ufe0f'  # 🗑️
        arrowup_symbol = '\U00002b06\ufe0f'  # ⬆️
        arrowdown_symbol = '\U00002b07\ufe0f' # ⬇️
        ok_symbol = '\U00002705' # ✅
        cancel_symbol = '\U0000274c' # ❌
        settings_symbol = '\U00002699\ufe0f' # ⚙️
        info_symbol = '\U00002139' # ℹ️
        warning_symbol = '\U000026a0\ufe0f' # ⚠️
        error_symbol = '\U0000274c' # ❌
        question_symbol = '\U00002753' # ❓
        folder_symbol = '\U0001f4c1' # 📁
        new_file_symbol = '\U0001f4c4' # 📄
        open_file_symbol = '\U0001f4c2' # 📂

    class UI:
        port: int = 8080
        listen: str = "0.0.0.0" # change this to 127.0.0.1 if you want to run it locally
        """If you want to use a custom theme other than the ones we or gradio provides, the class must be imported"""
        theme: gr.Theme = gr.themes.Default(
                            primary_hue="fuchsia",
                            secondary_hue="violet",
                            neutral_hue="neutral",
                            spacing_size="sm",
                            radius_size="none",
                        )

    class Compute:
        presicion: float = 0.001

        class CUDA:
            isAvailable: bool = False
            version: str = ""
            device: int = 0
            name: str = ""
            compute_capability: tuple = ()
            cores: int = 0
            memory: int = 0

        class CPU:
            name: str = ""
            cores: int = 0
            memory: int = 0

        useNativeCompute: bool = True
        fallbackCPUCompute: bool = True

    class Backends:
        class redis:
            host: str = "localhost"
            port: int = 6379
            db: int = 0

    project_folder: str = "./projects"




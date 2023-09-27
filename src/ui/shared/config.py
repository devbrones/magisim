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
        
    class UI:
        port: int = 8080
        theme: gr.Theme = gr.themes.Default(primary_hue="purple", secondary_hue="blue")

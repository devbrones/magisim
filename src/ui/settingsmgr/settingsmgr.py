import extensionmgr.extensionmgr as ExtensionManager
import gradio as gr

class SettingsManager:
    def get_settings_menu(app: gr.Blocks):
        # get installed extensions
        extensions = ExtensionManager.get_installed_extensions()
        print(extensions)
        for extension in extensions:
            # get extension settings eload
            extension_settings = ExtensionManager.get_extension_settings(extension)
            if extension_settings is not None or str:
                try:
                    extension_settings.load_workspace(app)
                except Exception as e:
                    print(e)
                    continue
            else:
                print("Error: Failed to load extension settings: " + extension)
                continue
            


class Project:
    """Magisims builtin project class"""
    loaded_extensions: list = []
    extension_data: dict = {}
    """extension_data is a dictionary with the following structure:
        {
            "<extension_uuid>": {
                "parameters": []
                "outputs": []
            },
            ...
        }
    an extension can also define its own data structure, but it must be a dictionary where the key
    is the extension uuid.
    """
    nmgr_data: dict = {} # node manager properties
    smgr_data: dict = {} # settings manager properties
    

    project_name: str = ""

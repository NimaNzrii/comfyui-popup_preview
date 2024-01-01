import importlib
import os
import subprocess
import folder_paths


import os

default_directory = os.getcwd()
node_path = os.path.join(folder_paths.get_folder_paths("custom_nodes")[0], "comfyui-popup_preview")
os.chdir(os.path.join(node_path, "window"))
if not os.path.exists(r".\venv"):
    os.system(r".\setup.bat")
os.chdir(default_directory)


try:
    import torchvision.transforms.functional as tf
    from PIL import ImageFile
except ImportError:
    subprocess.run(["python.exe", "-m", "pip", "install", "pillow"])
    subprocess.run(["python.exe", "-m", "pip", "install", "torch torchvision"])

node_list = [ 
    "popup"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module_name in node_list:
    imported_module = importlib.import_module(".{}".format(module_name), __name__)

    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
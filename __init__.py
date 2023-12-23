import importlib
import psutil
import os
import subprocess

os.chdir(r".\ComfyUI\custom_nodes\comfyui-popup_preview\window")
Python_patch = os.path.abspath(os.path.join(os.getcwd(), r"venv\Scripts\python.exe"))
if not os.path.exists(r".\venv"):
    os.system(r".\setup.bat")


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
import psutil
import os
from PIL import Image
import torch
import torchvision.transforms.functional as tf
from pathlib import Path
import tempfile
import folder_paths

node_path = os.path.join(folder_paths.get_folder_paths("custom_nodes")[0], "comfyui-popup_preview")
popup_window_path = os.path.join(node_path, 'window', 'popup_window.py')
python_path = os.path.join(node_path, 'window', 'venv', 'Scripts', 'python.exe')

def openWindow():
    Python_patch = os.path.abspath(python_path)
    python_running = any(p.info['exe'] == Python_patch for p in psutil.process_iter(['pid', 'name', 'exe']))
    
    if not python_running:
        import subprocess
        subprocess.Popen([Python_patch, popup_window_path])

def save_image(img: torch.Tensor, subpath):
    path = subpath

    if len(img.shape) == 4 and img.shape[0] == 1:
        img = img.squeeze(0)  
    if len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError(f"Input image must have 3 channels and a 3-dimensional shape, but got {img.shape}")

    img = img.permute(2, 0, 1)
    img = img.clamp(0, 1)
    img = tf.to_pil_image(img)
    
    img.save(path, format="PNG", compress_level=1)
    openWindow()
    


class PreviewPopup:
    INPUT_TYPES = lambda: { "required": { "image": ("IMAGE",) }, }
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "execute"
    CATEGORY = "ToyxyzTestNodes"

    def execute(
        self,
        image: torch.Tensor
    ):
        assert isinstance(image, torch.Tensor)

        OUTPUT_PATH = Path(tempfile.gettempdir()) / 'temp_image_preview.png'
        subpath = OUTPUT_PATH

        save_image(image, subpath)

        return ()

NODE_CLASS_MAPPINGS = {
    "PreviewPopup": PreviewPopup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewPopup": "PreviewPopup"
}
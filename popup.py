import psutil
import os
from PIL import Image
import torch
import torchvision.transforms.functional as tf
from pathlib import Path
import subprocess
import tempfile
import time
import numpy as np

def execute_after_save():
    Python_patch = os.path.abspath(os.path.join(os.getcwd(), r"venv\Scripts\python.exe"))
    if not [p.info for p in psutil.process_iter(['pid', 'name', 'exe']) if p.info['exe'] == Python_patch]:
        subprocess.Popen([Python_patch, 'popup_window.py'])

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
    execute_after_save()
    


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
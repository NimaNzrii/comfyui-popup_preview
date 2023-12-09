from PIL import ImageFile
import torch
import torchvision.transforms.functional as tf
from pathlib import Path
import subprocess
import tempfile

import time

last_execution_time = 0 

def execute_after_save():
    global last_execution_time 
    current_time = time.time()

    # بررسی زمان گذشته از آخرین اجرا
    if current_time - last_execution_time >= 5:
        subprocess.Popen("./ComfyUI/custom_nodes/comfyui-popup_preview/window/launcher.exe")
        last_execution_time = current_time 

ImageFile.LOAD_TRUNCATED_IMAGES = True

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
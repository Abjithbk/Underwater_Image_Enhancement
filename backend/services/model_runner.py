import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import os

from models.unet import UNet

class ModelRunner:
    """
    Wraps the U-Net model for inference.
    Created once when FastAPI starts.
    """
     
    def __init__(self,model_path:str = None):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print(f"Using device: {self.device}")

        self.model = UNet(in_channels=3,out_channels=3).to(self.device)

        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(
                torch.load(model_path,map_location = self.device)
            )

            print(f"Loaded weights from {model_path}")

        else:
             # No weights yet — uses random weights
            # Pipeline still works, quality will be poor
            # Day 3 training fixes this
            print("No weights found — using untrained model")
        
        self.model.eval()

        # Preprocessing pipeline: PIL → normalized tensor

        self.to_tensor = T.Compose(
            [
                T.to_tensor(),
                T.Normalize(
                    mean = [0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225] 
                )
            ]
        )
    
    def enhance(self,image:Image.Image) -> Image.Image:
        """
        Runs one image through the U-Net.
        Input:  PIL Image (256x256)
        Output: PIL Image (256x256) enhanced
        """

        # PIL → tensor, add batch dimension
        # (3,256,256) → (1,3,256,256)
        # model always expects a batch dimension
        tensor = self.to_tensor(image).unsqueeze(0).to(self.device)

        # no_grad = don't track gradients
        # we are inferencing not training
        # saves memory and runs faster
        with torch.no_grad():
            output = self.model(tensor)

        # Remove batch dimension: (1,3,256,256) → (3,256,256)
        output = output.squeeze(0).cpu().numpy()

        # Reverse the normalization we applied before
        mean = np.array([0.485, 0.456, 0.406])
        std  = np.array([0.229, 0.224, 0.225])

        # (3,H,W) → (H,W,3) because PIL expects channels last
        output = np.transpose(output, (1, 2, 0))

        # pixel = (normalized_value * std) + mean
        output = (output * std) + mean

        # Clip to valid range, convert to 0-255 integers
        output = np.clip(output, 0, 1)
        output = (output * 255).astype(np.uint8)

        return Image.fromarray(output)
         
     

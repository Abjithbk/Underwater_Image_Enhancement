import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import os

from models.unet import UNet

class ModelRunner:

    def __init__(self, model_path: str = None):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        print(f"Using device: {self.device}")

        self.model = UNet(in_channels=3, out_channels=3).to(self.device)

        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(
                torch.load(model_path, map_location=self.device)
            )
            print(f"Loaded weights from {model_path}")
        else:
            print("No weights found — using untrained model")

        self.model.eval()

        # Only ToTensor and Normalize — nothing else
        self.to_tensor = T.Compose([
            T.Resize((256, 256)),     # ensure correct size
            T.ToTensor(),             # PIL → tensor [0,1] shape (3,H,W)
            T.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def enhance(self, image: Image.Image) -> Image.Image:
        # Make sure image is RGB — exactly 3 channels
        if image.mode != "RGB":
            image = image.convert("RGB")

        # PIL → tensor → add batch dim
        # shape: (3,256,256) → (1,3,256,256)
        tensor = self.to_tensor(image).unsqueeze(0).to(self.device)

        print(f"Input tensor shape: {tensor.shape}")
        # should print: torch.Size([1, 3, 256, 256])

        with torch.no_grad():
            output = self.model(tensor)

        print(f"Output tensor shape: {output.shape}")

        # Remove batch dim: (1,3,256,256) → (3,256,256)
        output = output.squeeze(0).cpu().numpy()

        # (3,H,W) → (H,W,3)
        output = np.transpose(output, (1, 2, 0))

        # Denormalize
        mean = np.array([0.485, 0.456, 0.406])
        std  = np.array([0.229, 0.224, 0.225])
        output = (output * std) + mean

        # Clip and convert to uint8
        output = np.clip(output, 0, 1)
        output = (output * 255).astype(np.uint8)

        return Image.fromarray(output)
import torch
import torch.nn as nn
import torchvision.transforms as T
from PIL import Image
import numpy as np
import os


# MUST be same architecture as Colab!
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(x + self.block(x))


class UnderwaterNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(inplace=True),
        )

        self.res_blocks = nn.Sequential(
            ResidualBlock(64),
            ResidualBlock(64),
            ResidualBlock(64),
            ResidualBlock(64),
        )

        self.reconstruct = nn.Sequential(
            nn.Conv2d(64, 32, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 3, 3, padding=1),
        )

    def forward(self, x):
        feat       = self.features(x)
        res        = self.res_blocks(feat)
        correction = self.reconstruct(res)
        output     = x + torch.tanh(correction) * 0.3
        return torch.clamp(output, 0, 1)


class ModelRunner:

    def __init__(self, model_path: str = None):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        print(f"Using device: {self.device}")

        # Use UnderwaterNet — same as Colab!
        self.model = UnderwaterNet().to(self.device)

        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(
                torch.load(model_path, map_location=self.device)
            )
            print(f"✅ Loaded weights from {model_path}")
        else:
            print("⚠️ No weights found — using untrained model")

        self.model.eval()

        # NO normalization — same as Colab training!
        self.to_tensor = T.Compose([
            T.Resize((256, 256)),
            T.ToTensor()
            # No Normalize — matches training exactly
        ])

    def enhance(self, image: Image.Image) -> Image.Image:
        if image.mode != "RGB":
            image = image.convert("RGB")

        # PIL → tensor → add batch dim
        tensor = self.to_tensor(image).unsqueeze(0).to(self.device)
        print(f"Input tensor shape: {tensor.shape}")

        with torch.no_grad():
            output = self.model(tensor)

        print(f"Output tensor shape: {output.shape}")

        # Remove batch dim
        output = output.squeeze(0).cpu().numpy()

        # CHW → HWC
        output = np.transpose(output, (1, 2, 0))

        # NO denormalization needed!
        # Just clip and convert
        output = np.clip(output, 0, 1)
        output = (output * 255).astype(np.uint8)

        return Image.fromarray(output)
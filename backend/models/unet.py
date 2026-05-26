import torch
import torch.nn as nn


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class UNet(nn.Module):
    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 3,
        features: list = [64, 128, 256, 512]
    ):
        super().__init__()

        self.encoders = nn.ModuleList()
        self.pools    = nn.ModuleList()

        # build encoder levels
        ch = in_channels
        for f in features:
            self.encoders.append(DoubleConv(ch, f))
            self.pools.append(nn.MaxPool2d(2, 2))
            ch = f

        # bottleneck
        self.bottleneck = DoubleConv(features[-1], features[-1] * 2)

        # build decoder levels
        self.upconvs  = nn.ModuleList()
        self.decoders = nn.ModuleList()
        for f in reversed(features):
            self.upconvs.append(
                nn.ConvTranspose2d(f * 2, f, kernel_size=2, stride=2)
            )
            self.decoders.append(DoubleConv(f * 2, f))

        self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)
        self.sigmoid    = nn.Sigmoid()

    def forward(self, x):
        # x shape must be [batch, 3, 256, 256]
        print(f"  UNet input shape: {x.shape}")

        skip_connections = []

        # ENCODER — go down
        for i, (encoder, pool) in enumerate(zip(self.encoders, self.pools)):
            x = encoder(x)
            print(f"  After encoder {i}: {x.shape}")
            skip_connections.append(x)
            x = pool(x)
            print(f"  After pool {i}: {x.shape}")

        # BOTTLENECK
        x = self.bottleneck(x)
        print(f"  After bottleneck: {x.shape}")

        # DECODER — go up
        skip_connections = skip_connections[::-1]
        for i in range(len(self.decoders)):
            x    = self.upconvs[i](x)
            skip = skip_connections[i]

            if x.shape != skip.shape:
                x = nn.functional.interpolate(x, size=skip.shape[2:])

            x = torch.cat([skip, x], dim=1)
            x = self.decoders[i](x)
            print(f"  After decoder {i}: {x.shape}")

        return self.sigmoid(self.final_conv(x))
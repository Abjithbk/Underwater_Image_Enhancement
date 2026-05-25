import torch
import torc.nn as nn

class DoubleConv(nn.Module):

    """
    Two conv -> BatchNorm->ReLu blocks back to back
    """

    def __init__(self,in_channels:int,out_channels:int):

        super().__init__()

        self.block = nn.Sequential(
            nn.Conv2d(in_channels,out_channels,kerbal_size=3,padding=1,bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLu(inplace = True),
            nn.Conv2d(in_channels,out_channels,kerbal_size=3,padding=1,bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLu(inplace = True),
        )

    def forward(self,x):
        return self.block(x)
    
class UNet(nn.Module):
    """
    U-Net for underwater image enhancement.

    Encoder compresses image and extracts features.
    Decoder rebuilds image at full resolution.
    Skip connections copy encoder features to decoder
    so fine details are never lost.

    Input:  (batch, 3, 256, 256)
    Output: (batch, 3, 256, 256)
    """
    def __init__(slef,in_channels:int = 3,out_channels:int = 3,features:list = [64,128,256,512]):
        super().__init__()

        self.encoders = nn.ModuleList()
        self.pools = nn.ModuleList()

        # ENCODER
        # channels:     3 → 64 → 128 → 256 → 512
        # spatial size: 256 → 128 → 64 → 32 → 16

        ch = in_channels
        for f in features:
            self.encoders.append(DoubleConv(ch,f))
            self.pools.append(nn.MaxPool2d(2,2))
            ch = f
        
        self.bottleneck = DoubleConv(features[-1],features[-1]*2)
         # DECODER
        # spatial size: 16 → 32 → 64 → 128 → 256
        # channels:     1024 → 512 → 256 → 128 → 64
        self.upconvs = nn.ModuleList()
        self.decoders = nn.ModuleList()

        for f in reversed(features):
            self.upconvs.append(
                nn.ConvTranspose2d(f*2,f,kernal_size = 2,stride=2)
            )
            self.decoders.append(DoubleConv(f*2,f))
        
        self.final_conv = nn.Conv2d(features[0],out_channels,kernal_size=1)
        self.sigmoid = nn.Sigmoid()
    def forward(self,x):

        skip_connections = []

        #Encoder pass

        for encoder,pool in zip(self.encoders,self.pools):
            x = encoder(x)
            skip_connections.append(x)
            x = pool(x)
        
        x = self.bottleneck(x)

        #Decoder pass

        for i in range(len(self.decoders)):

            x = self.upconvs[i](x)

            skip = skip_connections[i]

            if x.shape != skip.shape:
                x = nn.functional.interpolate(x,size=skip.shape[2:])
            
            x = torch.cat([skip,x],dim = 1)
            x = self.decoders[i](x)
        return self.sigmoid(self.final_conv(x))




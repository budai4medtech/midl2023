import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from model.SwinTransformer import SwinTransformerLayer
from model.utils import Upsample, EqualLinear


class ToIMG(nn.Module):
    def __init__(self, in_c, upsample=True, blur_kernel=[1, 3, 3, 1]):
        super().__init__()
        self.is_upsample = upsample
        if upsample:
            self.upsample = Upsample(blur_kernel)
        self.conv = nn.Conv2d(in_c, 1, 1, bias=False)
        self.bias = nn.Parameter(torch.zeros(1, 1, 1, 1))
    def forward(self, x, skip=None):
        out = self.conv(x)
        out = out + self.bias

        if skip is not None:
            if self.is_upsample:
                skip = self.upsample(skip)
            out = out + skip
        return out


class ConstantInput(nn.Module):
    def __init__(self, channel, size=4):
        super().__init__()
        self.input = nn.Parameter(torch.randn(1, channel, size, size))

    def forward(self, x):
        batch = x.shape[0]
        out = self.input.repeat(batch, 1, 1, 1)
        return out


class Generator(nn.Module):

    def __init__(self, img_size, n_channel, latent_dim=512):
        super().__init__()
        self.img_size = img_size
        self.channel = n_channel
        self.latent_dim = latent_dim
        self.style = nn.Sequential(*[
            EqualLinear(latent_dim, latent_dim, lr_mul=0.01, activation='fused_lrelu')
            for _ in range(8)
        ])
        self.n_latent = 12
        self.input = ConstantInput(512)
        self.swinlayers = nn.ModuleList([
            SwinTransformerLayer(dim=512, input_resolution=(4, 4), depth=2,
                                 num_heads=16, window_size=4, out_dim=512,
                                 upsample=True),
            SwinTransformerLayer(dim=512, input_resolution=(8, 8), depth=2,
                                 num_heads=16, window_size=8, out_dim=256,
                                 upsample=True),
            SwinTransformerLayer(dim=256, input_resolution=(16, 16), depth=2,
                                 num_heads=8, window_size=8, out_dim=128,
                                 upsample=True),
            SwinTransformerLayer(dim=128, input_resolution=(32, 32), depth=2,
                                 num_heads=4, window_size=8, out_dim=64,
                                 upsample=True),
            SwinTransformerLayer(dim=64, input_resolution=(64, 64), depth=2,
                                 num_heads=4, window_size=8, out_dim=32,
                                 upsample=True),
            SwinTransformerLayer(dim=32, input_resolution=(128, 128), depth=2,
                                 num_heads=4, window_size=8)
        ])
        self.skip = nn.ModuleList([
            ToIMG(512),
            ToIMG(256),
            ToIMG(128),
            ToIMG(64),
            ToIMG(32),
            ToIMG(32, upsample=False),
        ])
        
        self.final_layer = nn.Sequential(
            nn.Tanh()
        )
        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            nn.init.trunc_normal_(m.weight, std=.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
            if m.weight is not None:
                nn.init.constant_(m.weight, 1.0)
        elif isinstance(m, nn.Conv2d):
            nn.init.xavier_normal_(m.weight, gain=.02)
            if hasattr(m, 'bias') and m.bias is not None:
                nn.init.constant_(m.bias, 0)
            
    def pixel_norm(self, z):
        return z * torch.rsqrt(torch.mean(z ** 2, dim=1, keepdim=True) + 1e-8)

    def forward(self, z):
        styles = self.style(self.pixel_norm(z))
        inject_index = self.n_latent
        if styles.ndim < 3:
            latent = styles.unsqueeze(1).repeat(1, inject_index, 1)
        else:
            latent = styles
        x = self.input(latent)
        B, C, H, W = x.shape
        x = x.permute(0, 2, 3, 1).contiguous().view(B, H * W, C)
        
        count = 0
        skip = None
        
        for layer, to_img in zip(self.swinlayers, self.skip):
            x = layer(x, latent[:,count,:], latent[:,count+1,:])
            B, L, C = x.shape
            H = W = int(np.sqrt(L))
            skip = to_img(x.transpose(-1, -2).reshape(B, C, H, W), skip)
        
        return self.final_layer(skip).to('cuda')

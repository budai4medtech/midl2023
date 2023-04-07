# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# From article: [CVPR 2022] StyleSwin: Transformer-based GAN for High-resolution Image Generation. arXiv:2112.10762
# Github Repository: https://github.com/microsoft/StyleSwin


import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from model.utils import Downsample, Blur, EqualConv2d, EqualLinear
from utils_nvidia.upfirdn2d import upfirdn2d
from utils_nvidia.fused_act import FusedLeakyReLU


def get_haar_wavelet(in_channels):
    haar_wav_l = 1 / (2 ** 0.5) * torch.ones(1, 2)
    haar_wav_h = 1 / (2 ** 0.5) * torch.ones(1, 2)
    haar_wav_h[0, 0] = -1 * haar_wav_h[0, 0]

    haar_wav_ll = haar_wav_l.T * haar_wav_l
    haar_wav_lh = haar_wav_h.T * haar_wav_l
    haar_wav_hl = haar_wav_l.T * haar_wav_h
    haar_wav_hh = haar_wav_h.T * haar_wav_h
    
    return haar_wav_ll, haar_wav_lh, haar_wav_hl, haar_wav_hh


class HaarTransform(nn.Module):
    def __init__(self, in_channels):
        super().__init__()

        ll, lh, hl, hh = get_haar_wavelet(in_channels)

        self.register_buffer('ll', ll)
        self.register_buffer('lh', lh)
        self.register_buffer('hl', hl)
        self.register_buffer('hh', hh)

    def forward(self, img):
        ll = upfirdn2d(img, self.ll, down=2)
        lh = upfirdn2d(img, self.lh, down=2)
        hl = upfirdn2d(img, self.hl, down=2)
        hh = upfirdn2d(img, self.hh, down=2)

        return torch.cat((ll, lh, hl, hh), 1)


class InverseHaarTransform(nn.Module):
    def __init__(self, in_channels):
        super().__init__()

        ll, lh, hl, hh = get_haar_wavelet(in_channels)
        self.register_buffer('ll', ll)
        self.register_buffer('lh', -lh)
        self.register_buffer('hl', -hl)
        self.register_buffer('hh', hh)

    def forward(self, img):
        ll, lh, hl, hh = img.chunk(4, 1)
        ll = upfirdn2d(ll, self.ll, up=2, pad=(1, 0, 1, 0))
        lh = upfirdn2d(lh, self.lh, up=2, pad=(1, 0, 1, 0))
        hl = upfirdn2d(hl, self.hl, up=2, pad=(1, 0, 1, 0))
        hh = upfirdn2d(hh, self.hh, up=2, pad=(1, 0, 1, 0))

        return ll + lh + hl + hh
    

class FromRGB(nn.Module):
    def __init__(self, out_channel, downsample=True, blur_kernel=[1, 3, 3, 1]):
        super().__init__()

        self.downsample = downsample

        if downsample:
            self.iwt = InverseHaarTransform(1)
            self.downsample = Downsample(blur_kernel)
            self.dwt = HaarTransform(1)

        self.conv = nn.Sequential(
            EqualConv2d(4, out_channel, 1, bias=False),
            nn.LeakyReLU(0.2)
        )

    def forward(self, x, skip=None):
        if self.downsample:
            x = self.iwt(x)
            x = self.downsample(x)
            x = self.dwt(x)
        out = self.conv(x)
        if skip is not None:
            out = out + skip
        return x, out


class DiscBlock(nn.Module):
    def __init__(self, in_c, out_c, downsample=True, blur_kernel=[1, 3, 3, 1]):
        super().__init__()
        self.is_downsample = downsample
        if downsample:
            factor = 2
            p = (len(blur_kernel) - factor) + 2
            pad0 = (p + 1) // 2
            pad1 = p // 2
            self.blur = Blur(blur_kernel, pad=(pad0, pad1))
            self.stride = 2
            self.padding = 0
        else:
            self.stride = 1
            self.padding = 1

        self.conv1 = EqualConv2d(in_c, in_c, kernel_size=3, padding=1, bias=False)
        self.act1 = FusedLeakyReLU(in_c)
        self.conv2 = EqualConv2d(in_c, out_c, kernel_size=3, stride=self.stride, padding=self.padding, bias=False)
        self.act2 = FusedLeakyReLU(out_c)

    def forward(self, x):
        x = self.act1(self.conv1(x))
        if self.is_downsample:
            x = self.blur(x)
        x = self.act2(self.conv2(x))
        return x


class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.dwt = HaarTransform(1)
        self.conv = nn.ModuleList([
            DiscBlock(256, 512),
            DiscBlock(512, 512),
            DiscBlock(512, 512),
            DiscBlock(512, 512),
            DiscBlock(512, 512),
        ])
        
        self.skip = nn.ModuleList([
            FromRGB(256, downsample=False), # 256
            FromRGB(512),
            FromRGB(512),
            FromRGB(512),
            FromRGB(512),
            FromRGB(512)
        ])

        self.stddev_group = 4
        self.stddev_feat = 1
        self.final_conv = EqualConv2d(512+1, 512, 3, stride=1, padding=1, bias=False)
        self.final_linear = nn.Sequential(
            EqualLinear(512 * 4 * 4, 512, activation='fused_lrelu'),
            EqualLinear(512, 1),
        )

        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Conv2d):
            nn.init.xavier_uniform_(module.weight, gain=0.02)
        elif isinstance(module, nn.Linear):
            nn.init.trunc_normal_(module.weight, std=.02)

    def forward(self, img):
        img = self.dwt(img)
        out = None
        for from_rgb, conv in zip(self.skip, self.conv):
            img, out = from_rgb(img, out)
            out = conv(out)
        _, out = self.skip[-1](img, out)

        B, C, H, W = out.shape
        group = min(B, self.stddev_group)
        stddev = out.view(group, -1, self.stddev_feat, C // self.stddev_feat, H, W)
        stddev = torch.sqrt(stddev.var(0, unbiased=False) + 1e-8)
        stddev = stddev.mean([2, 3, 4], keepdims=True).squeeze(2)
        stddev = stddev.repeat(group, 1, H, W)
        out = torch.cat([out, stddev], 1)
        out = self.final_conv(out)
        out = out.view(B, -1)
        out = self.final_linear(out)

        return out

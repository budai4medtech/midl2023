# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# From article: [CVPR 2022] StyleSwin: Transformer-based GAN for High-resolution Image Generation. arXiv:2112.10762
# Github Repository: https://github.com/microsoft/StyleSwin


import math
import torch
from torch import nn
from torch.nn import functional as F
from utils_nvidia.upfirdn2d import upfirdn2d
from utils_nvidia.fused_act import *

class Blur(nn.Module):
    def __init__(self, kernel, pad, upsample_factor=1):
        super().__init__()
        kernel = make_kernel(kernel)
        if upsample_factor > 1:
            kernel = kernel * (upsample_factor ** 2)
        self.register_buffer('kernel', kernel)
        self.pad = pad
    def forward(self, img):
        out = upfirdn2d(img, self.kernel, pad=self.pad)
        return out

def make_kernel(k):
    k = torch.tensor(k, dtype=torch.float32)
    if k.ndim == 1:
        k = k[None, :] * k[:, None]
    k /= k.sum()
    return k


class Upsample(nn.Module):
    def __init__(self, kernel, factor=2):
        super().__init__()
        self.factor = factor
        kernel = make_kernel(kernel) * (factor ** 2)
        self.register_buffer('kernel', kernel)
        p = kernel.shape[0] - factor
        pad0 = (p + 1) // 2 + factor - 1
        pad1 = p // 2
        self.pad = (pad0, pad1)

    def forward(self, img):
        out = upfirdn2d(img, self.kernel, up=self.factor, down=1, pad=self.pad)
        return out


class Downsample(nn.Module):
    def __init__(self, kernel, factor=2):
        super().__init__()
        self.factor = factor
        kernel = make_kernel(kernel)
        self.register_buffer('kernel', kernel)
        p = kernel.shape[0] - factor
        pad0 = (p + 1) // 2
        pad1 = p // 2
        self.pad = (pad0, pad1)

    def forward(self, input):
        out = upfirdn2d(input, self.kernel, up=1, down=self.factor, pad=self.pad)
        return out

    
class EqualConv2d(nn.Module):
    def __init__(
        self, in_channel, out_channel, kernel_size, stride=1, padding=0, bias=True
    ):
        super().__init__()

        self.weight = nn.Parameter(
            torch.randn(out_channel, in_channel, kernel_size, kernel_size)
        )
        self.scale = 1 / math.sqrt(in_channel * kernel_size ** 2)

        self.stride = stride
        self.padding = padding

        if bias:
            self.bias = nn.Parameter(torch.zeros(out_channel))

        else:
            self.bias = None

    def forward(self, x):
        out = F.conv2d(
            x,
            self.weight * self.scale,
            bias=self.bias,
            stride=self.stride,
            padding=self.padding,
        )

        return out

    
class EqualLinear(nn.Module):
    def __init__(
        self, in_dim, out_dim, bias=True, bias_init=0, lr_mul=1, activation=None
    ):
        super().__init__()

        self.weight = nn.Parameter(torch.randn(out_dim, in_dim).div_(lr_mul))

        if bias:
            self.bias = nn.Parameter(torch.zeros(out_dim).fill_(bias_init))

        else:
            self.bias = None

        self.activation = activation

        self.scale = (1 / math.sqrt(in_dim)) * lr_mul
        self.lr_mul = lr_mul

    def forward(self, input):
        if self.activation:
            out = F.linear(input, self.weight * self.scale)
            out = fused_leaky_relu(out, self.bias * self.lr_mul)

        else:
            out = F.linear(
                input, self.weight * self.scale, bias=self.bias * self.lr_mul
            )
        return out

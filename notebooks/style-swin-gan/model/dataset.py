import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset
from torchvision.transforms import (Compose, Resize, ToTensor, Normalize)


class ImageDataset(Dataset):
    """
    A customized dataset class that loads images from folder from pytorch.
    args:
    - df: pre-processed dataframe
    - directory: location of the images
    - transform: transform function to apply to the images
    - extension: file format
    """
    def __init__(self,
                 name_lst,
                 transforms=None,
                 directory='data/images/Images',
                 extension='.png'):
        self.img_names = name_lst
        self.transforms = transforms
        self.directory = directory
        self.extension = extension

    def __len__(self):
        """ returns the number of items in the dataset """
        return self.img_names.shape[0]

    def __getitem__(self, idx):
        """ load an image and apply transformation """
        image_path = os.path.join(
            self.directory,
            self.img_names[idx] + self.extension)
        image = Image.open(image_path)
        if self.transforms:
            image = self.transforms(image)
        return image


def denormalize(image):
    return ((image + 1.) / 2. * 255).type(torch.uint8)


def getDataset(plane_name, data_path='data/images/', size=256, show_img=False):

    transforms = Compose([
        Resize((size, size)),
        ToTensor(),
        Normalize([0.5], [0.5])    # ([0~1] - 0.5) / 0.5
    ])

    lst = np.load(f'{data_path+plane_name}.npy', allow_pickle=True)
    training_data = ImageDataset(lst, transforms)

    if show_img:
        fig = plt.figure(figsize=(12, 4))
        plot_size = 12
        for idx in np.arange(plot_size):
            ax = fig.add_subplot(2, int(plot_size/2), idx+1, xticks=[], yticks=[])
            img = denormalize(training_data[idx][0]).squeeze().numpy()
            ax.imshow(img, cmap='gray')

        plt.show()
        plt.clf()

    return training_data

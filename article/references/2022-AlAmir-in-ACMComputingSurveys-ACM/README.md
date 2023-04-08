# 
## Citations
3

https://scholar.google.com/scholar?cites=16552017953337845700&as_sdt=2005&sciodt=0,5&hl=en

Retrived
Sat 24 Sep 19:07:39 BST 2022

## Authors 

## Notes


> Lesion detection from images demands a tremendous amount of labeled training data [219]. GAN handles this
issue in two ways: (i) by improving the dataset with generated images and then applying traditional detection
models as in [63, 189], or (ii) by modeling distribution from which lesions can be recognized as outliers. The GAN’s
discriminator can be used to identify lesions by training on images representing normal pathology and learning
the probability distribution of these images. Chen and Konukoglu [32] utilized an adversarial auto-encoder
(AAE) and VAE to identify abnormalities according to the learned data distribution of healthy brain MRI images.
The learned latent space can be used to map the lesion image to an image without a lesion before computing
the residual of these two images in order to highlight the lesion. Xie et al. [208] proposed an approach for
detecting the fundus disease. The generator was designed in two parts: (i) attention encoder (AE) module, and (ii)
generation module. The AE module encodes the real images to extract the feature of shallow layers, whereas the
generation module produces the fake images by handling the input random noise by a set of the residual blocks
with upsampling (RU) operations. The discriminator is developed by using a multi-branch ResNet-34 frame to
extract the deep feature and for high-level feature extraction, the deep-wise asymmetric dilated convolution
(DADC) module has been used. The discriminator’s last layer has been modiied to build a classiier to detect the
diseased and normal images. Alex et al. [7] utilized GAN for the detection of a brain lesion on an MRI image,
where the G produces the sample by modeling the distribution of normal patches and the D allocates a higher
posterior probability of being real when compared to patches from various distributions (non-lesion patches).



## Links 

## Bibtex 

```
@article{10.1145/3527849,
author = {AlAmir, Manal and AlGhamdi, Manal},
title = {The Role of Generative Adversarial Network in Medical Image Analysis: An in-Depth Survey},
year = {2022},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
issn = {0360-0300},
url = {https://doi.org/10.1145/3527849},
doi = {10.1145/3527849},
abstract = {A generative adversarial network (GAN) is one of the most significant research directions in the field of artificial intelligence, and its superior data generation capability has garnered wide attention. In this paper, we discuss the recent advancements in GANs, particularly in the medical field. First, the different medical imaging modalities and the principal theory of GANs were analyzed and summarized, after which, the evaluation metrics and training issues were determined. Third, the extension models of GANs were classified and introduced one by one. Fourth, the applications of GAN in medical images including cross-modality, augmentation, detection, classification, and reconstruction were illustrated. Finally, the problems we needed to resolve, and future directions were discussed. The objective of this review is to provide a comprehensive overview of the GAN, simplify the GAN’s basics, and present the most successful applications in different scenarios.},
note = {Just Accepted},
journal = {ACM Comput. Surv.},
month = {mar},
keywords = {computer vision, medical image analysis, generative adversarial network}
}


```


# Datasets

## FETAL_PLANES_DB (2.1 GB): Common maternal-fetal ultrasound images

A large dataset of routinely acquired maternal-fetal screening ultrasound images collected from two different hospitals by several operators and ultrasound machines. All images were manually labeled by an expert maternal fetal clinician. Images are divided into 6 classes: four of the most widely used fetal anatomical planes (Abdomen, Brain, Femur and Thorax), the mother’s cervix (widely used for prematurity screening) and a general category to include any other less common image plane. Fetal brain images are further categorized into the 3 most common fetal brain planes (Trans-thalamic, Trans-cerebellum, Trans-ventricular) to judge fine grain categorization performance. Meta information (patient number, us machine, operator) is also provided, as well as the training-test split used in the Nature Sci Rep paper.

The research leading to these results has received funding from Transmural Biotech SL, "LaCaixa" Foundation under grant agreements LCF/PR/GN14/10270005 and LCF/PR/GN18/10310003 the Instituto de Salud Carlos III (PI16/00861, PI17/00675) within the Plan Nacional de I+D+I and cofinanced by ISCIII-Subdirección General de Evaluación together with the Fondo Europeo de Desarrollo Regional (FEDER) "Una manera de hacer Europa", Cerebra Foundation for the Brain Injured Child (Carmarthen, Wales, UK), Cellex Foundation and AGAUR under grant 2017 SGR nº 1531. Additionally, EE has received funding from the Departament de Salut under grant SLT008/18/00156. 

The final dataset is comprised of over 12,400 images from 1,792 patients. https://zenodo.org/record/3904280

If you find this dataset useful, please cite:

    @article{Burgos-ArtizzuFetalPlanesDataset,
      title={Evaluation of deep convolutional neural networks for automatic classification of common maternal fetal ultrasound planes},
      author={Burgos-Artizzu, X.P. and Coronado-Gutiérrez, D. and Valenzuela-Alcaraz, B. and Bonet-Carne, E. and Eixarch, E. and Crispi, F. and Gratacós, E.},
      journal={Nature Scientific Reports}, 
      volume={10},
      pages={10200},
      doi="10.1038/s41598-020-67076-5",
      year={2020}
    } 



* Notes
	* "Fetal brain images are further categorized into the 3 most common fetal brain planes (Trans-thalamic, Trans-cerebellum, Trans-ventricular) to judge fine grain categorization performance."

## path tree 
```
$ tree -fs
[       4096]  .
├── [     909943]  ./FETAL_PLANES_DB_data.csv
└── [     708608]  ./Images
    ├── [     197528]  ./Images/Patient00001_Plane1_10_of_15.png
    ├── [     298355]  ./Images/Patient00001_Plane1_11_of_15.png
    ├── [     307171]  ./Images/Patient00001_Plane1_12_of_15.png
    ├── [     288376]  ./Images/Patient00001_Plane1_13_of_15.png
    ├── [     263471]  ./Images/Patient00001_Plane1_14_of_15.png

	...

    ├── [     181924]  ./Images/Patient01791_Plane5_1_of_1.png
    ├── [     214864]  ./Images/Patient01792_Plane2_1_of_1.png
    ├── [     227836]  ./Images/Patient01792_Plane3_1_of_1.png
    ├── [     217875]  ./Images/Patient01792_Plane5_1_of_1.png
    └── [     206491]  ./Images/Patient01792_Plane6_1_of_1.png

1 directory, 12401 files
```


# Creating virtual environments

## Conda
Install [conda](https://github.com/mxochicale/code/tree/main/conda) and create [febusisVE](febusisVE.yml).

## Dependencies

* Python package versions
```
$ cd $HOME/.../dependencies
$ conda activate febusisVE
$ python package_versions.py 

python: 3.10.9 (main, Jan 11 2023, 15:21:40) [GCC 11.2.0]
torch: 1.11.0
torchvision: 0.12.0
torch cuda_is_available: True
torch cuda version: 11.3
torch cuda.device_count  1
PIL: 9.4.0

```
* OS
```
$ hostnamectl

 Static hostname: --
       Icon name: computer-laptop
         Chassis: laptop
      Machine ID: --
         Boot ID: --
Operating System: Ubuntu 22.04.1 LTS              
          Kernel: Linux 5.15.0-56-generic
    Architecture: x86-64
 Hardware Vendor: --

```
* GPU
```
$ nvidia-smi -q

==============NVSMI LOG==============

Timestamp                                 : Sat Dec 17 13:27:52 2022
Driver Version                            : 520.61.05
CUDA Version                              : 11.8

Attached GPUs                             : 1
GPU 00000000:01:00.0
    Product Name                          : NVIDIA RTX A2000 8GB Laptop GPU
    Product Brand                         : NVIDIA RTX
    Product Architecture                  : Ampere

```



## Sort of automatic creation 

### Creation
Using `env.yml` create an environment
```
conda deactivate
conda env create -f ${YML_FILENAME}.yml
conda activate synthetic-fetus-ve-cpu #OR conda activate synthetic-fetus-ve-gpu
```

### Update env
```
conda env update --file ${YML_FILENAME}.yml  --prune
conda activate ${NAME_OF_VE}
```
"The --prune option causes conda to remove any dependencies that are no longer required from the environment."
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html


### Run env 
Open a terminal and run: 
```
conda activate simple-virtual-environment
```

## rename virtual environment

```
conda create --name new_name --copy --clone old_name
conda remove --name old_name --all # or its alias: `conda env remove --name old_name`
```
example
```
conda create --name ve-python38-cuda11 --copy --clone ve-python38-cuda112
conda remove --name ve-python38-cuda112 --all
```

## list env

You can list all discoverable environments with `conda info --envs`.

## Manual creation 
* create an virtual environment
```
cd
conda create -n testing python=3.6 pip numpy #remember to initialize the env with pip here.
```


* activate the virtual environment
```
conda activate testing
```


* deactivate your tensorflow conda env 
```
conda deactivate
conda deactivate
```


* delete a no longer needed virtual environmnet
```
conda remove -n testing --all
```


## Learn more
* https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/
* https://medium.freecodecamp.org/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c



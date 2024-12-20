
# A comedy handbook

## Team

ADAptables :

Arthur Removille, Caroline Verchère, Quentin Gallien, Théo Le Blan, Victor Garvalov

## Repository presentation
This repository contains the code used for our project titled "A comedy Handbook". You can read the data story [here](https://epfl-ada.github.io/ada-2024-project-adaptables/). All the code used to generate the various graphs and conclusions in it can be obtained by reading through the [results notebook](results.ipynb).

## Quickstart

This project was run using Python 3.10.12. We cannot provide certainty that other versions will work (though anything newer should be fine). Some of our code elegantly uses Python's [pattern matching](https://peps.python.org/pep-0636/), which was introduced in 3.10. Earlier Python versions will therefore not work out of the box (but can be adapted by making very small changes).

**Important note!**

One of the additional datasets we are using is too large to be hosted on Git, and we cannot use Git LFS as the repossitory is tied to one owner - the organization. As such, please download it manually from [here](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews), and place the `rotten_tomatoes_movie_reviews.csv` under `data/raw/`.

Furthermore, the aforementionned file and some of the files needed to recreate our graphs (`data/processed/`) are too big for GitHub. We therefore saved them in a zip which you can download from [here](https://go.epfl.ch/adaptables_extra_files). Simply extract it (`unzip extra_files.zip`) inside the root directory, and all the files will place themselves. 

```bash
# clone project
git clone git@github.com:epfl-ada/ada-2024-project-adaptables.git
cd ada-2024-project-adaptables

# [OPTIONAL] create conda environment
# conda create -n <env_name> python=3.11 or ...
# conda activate <env_name>

# [OR, OPTIONAL] create venv
python3 -m venv venv
source venv/bin/activate        # POSIX (Linux, MAC ; bash)
# venv/Scripts/activate.bat     # Windows (cmd)
# venv/Scripts/Activate.ps1     # Windows (PS)

# install requirements
pip install -r pip_requirements.txt
```

## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Datasets
│   ├── raw                             <- raw files (for subset of smaller datasets)
│   ├── processed                       <- pre-processed datasets (see below)
│
├── src                         <- Source code
│   ├── data                            <- Dataloaders/datamodules code 
│   ├── models                          <- Model directory (TODO: custom KeyBert)
│   ├── plots                           <- Utilitary functions used to generate all our plots
│   ├── scripts                         <- Python scripts used to recreate some of the pre-processed data (see below)
│   ├── utils                           <- Utility directory
│
├── personal_work               <- Temporary directory for M2 with individual work - can be safely ignored (TODO remove)
│
├── results.ipynb               <- The main notebook showing the results and conclusions used in our data story
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md

```

The `data/processed` folder contains some intermediate pre-computed data which takes more time to get. See its [README](data/processed/README.md) to understand what to do to recreate it.  